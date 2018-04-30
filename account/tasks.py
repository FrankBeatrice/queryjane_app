import logging

from django.conf import settings
from django.template.loader import render_to_string
from huey import crontab
from huey.contrib.djhuey import db_periodic_task

from account.models import ProfessionalProfile
from account.models import UserMessage
from app.tasks import send_email


logger = logging.getLogger('huey.consumer')


@db_periodic_task(crontab(day_of_week='1,3,5', hour='7', minute='0'))
def new_received_messages():
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

                    messages_dict[key] = [contact_dict]
            else:
                # Creating key to group messages from users
                # to display them in the email detail. The used
                # format is u_user_id.
                key = 'u_{}'.format(new_message.company_from.id)

                if key in messages_dict:
                    messages_dict[key]['messages'].append(new_message)
                else:
                    contact_dict = {
                        'name': new_message.user_from.get_full_name(),
                        'messages': [new_message],
                    }

                    messages_dict[key] = [new_message]

        subject = 'You have {0} new messages in your inbox'.format(
            new_messages,
        )

        body = render_to_string(
            'account/emails/new_messages.html', {
                'title': subject,
                'message': messages_dict,
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
