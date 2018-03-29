import logging

from django.conf import settings
from django.template.loader import render_to_string
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from account.data import NEW_APPLICANTS
from account.models import UserNotification
from app.tasks import send_email
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import JOB_STATUS_ACTIVE
from entrepreneur.models import JobOffer


logger = logging.getLogger('huey.consumer')


@db_periodic_task(crontab(day_of_week='1,4', hour='6', minute='0'))
def new_applicants_notifications():
    for job_offer in JobOffer.objects.filter(status=JOB_STATUS_ACTIVE):
        applicants_record = job_offer.applicants_record
        current_applicants = job_offer.applicant_set.count()

        new_applicants = current_applicants - applicants_record

        if new_applicants:
            # admins_m = admin memberships
            admins_m = job_offer.venture.administratormembership_set.filter(
                status=ACTIVE_MEMBERSHIP,
            )

            for admin_m in admins_m:
                # Send email notification.
                if admin_m.admin.new_applicants_notifications:
                    subject = '{0} new applicants to your job offer.'.format(
                        new_applicants,
                    )

                    body = render_to_string(
                        'entrepreneur/emails/new_applicants.html', {
                            'title': subject,
                            'job_offer': job_offer,
                            'new_applicants': new_applicants,
                            'base_url': settings.BASE_URL,
                        },
                    )

                    send_email(
                        subject=subject,
                        body=body,
                        mail_to=[admin_m.admin.user.email],
                    )

                description = 'New applicants to "{}".'.format(
                    job_offer,
                )

                # Create platform notification.
                UserNotification.objects.create(
                    notification_type=NEW_APPLICANTS,
                    noty_to=admin_m.admin.user,
                    answered=True,
                    job_offer=job_offer,
                    venture_from=job_offer.venture,
                    description=description,
                )

                logger.info(
                    'Created notifications to %s',
                    admin_m.admin.user.email,
                )

        job_offer.applicants_record = current_applicants
        job_offer.save()
