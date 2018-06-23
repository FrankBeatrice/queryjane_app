import logging

from django.conf import settings
from django.template.loader import render_to_string
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from account.models import ProfessionalProfile
from account.models import UserMessage
from app.tasks import send_email
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import OWNER
from entrepreneur.data import QJANE_ADMIN
from entrepreneur.models import Venture


logger = logging.getLogger('huey.consumer')


@db_periodic_task(crontab(day_of_week='1,3,5', hour='7', minute='0'))
def new_received_messages():
    """
    Peridoic task that runs all Mondays, Wednesdays and Fridays at 7:00 am.
    This tasks checks if users have new private messages and creates a
    notification to inform them about new messages.
    """
    for professionalprofile in ProfessionalProfile.objects.filter(
        has_new_messages=True,
        email_messages_notifications=True,
    ):
        # Get new messages
        new_messages = UserMessage.objects.filter(
            user_to=professionalprofile.user,
            unread=True,
        )

        messages_dict = {}

        for new_message in new_messages:
            if new_message.company_from:
                # Creating key to group messages from companies
                # to display them in the email detail. The used
                # format is c_company_id.
                key = 'c_{}'.format(new_message.company_from.id)

                if key in messages_dict:
                    messages_dict[key]['messages'].append(new_message)
                else:
                    contact_dict = {
                        'name': new_message.company_from.name,
                        'messages': [new_message],
                    }

                    messages_dict[key] = contact_dict
            else:
                # Creating key to group messages from users
                # to display them in the email detail. The used
                # format is u_user_id.
                key = 'u_{}'.format(new_message.user_from.id)

                if key in messages_dict:
                    messages_dict[key]['messages'].append(new_message)
                else:
                    contact_dict = {
                        'name': new_message.user_from.get_full_name,
                        'messages': [new_message],
                    }

                    messages_dict[key] = contact_dict

        subject = 'You have {0} new messages in your inbox'.format(
            new_messages.count(),
        )

        body = render_to_string(
            'account/emails/new_messages.html', {
                'title': subject,
                'to_user': True,
                'receiver': professionalprofile.user,
                'messages_dict': messages_dict,
                'base_url': settings.BASE_URL,
            },
        )

        send_email(
            subject=subject,
            body=body,
            mail_to=[professionalprofile.user.email],
        )

        professionalprofile.has_new_messages = False
        professionalprofile.save()

    for company in Venture.objects.filter(
        has_new_messages=True,
    ):
        # Get new messages
        new_messages = UserMessage.objects.filter(
            company_to=company,
            unread=True,
        )

        messages_dict = {}

        for new_message in new_messages:
            # Creating key to group messages from users
            # to display them in the email detail. The used
            # format is u_user_id.
            key = 'u_{}'.format(new_message.user_from.id)

            if key in messages_dict:
                messages_dict[key]['messages'].append(new_message)
            else:
                contact_dict = {
                    'name': new_message.user_from.get_full_name,
                    'messages': [new_message],
                }

                messages_dict[key] = contact_dict

        description = '{0} has {1} new messages'.format(
            company,
            new_messages.count(),
        )

        # Create new message notification for company administrators.
        for membership in company.administratormembership_set.filter(
            status=ACTIVE_MEMBERSHIP,
            role__in=(OWNER, QJANE_ADMIN),
        ):
            user = membership.admin.user

            if user.professionalprofile.new_company_messages_notifications:
                subject = description

                body = render_to_string(
                    'account/emails/new_messages.html', {
                        'title': subject,
                        'company_to': company,
                        'receiver': user,
                        'messages_dict': messages_dict,
                        'base_url': settings.BASE_URL,
                    },
                )

                send_email(
                    subject=subject,
                    body=body,
                    mail_to=[user.email],
                )

        company.has_new_messages = False
        company.save()
