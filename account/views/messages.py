from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import View

from account.data import NEW_MESSAGE_TO_COMPANY
from account.forms import UserMessageForm
from account.models import User
from account.models import UserMessage
from account.models import UserNotification
from account.permissions import MessagesPermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import OWNER
from entrepreneur.data import QJANE_ADMIN
from entrepreneur.models import Venture
from entrepreneur.permissions import EntrepreneurPermissions


class InboxView(LoginRequiredMixin, ListView):
    model = UserMessage
    template_name = 'account/inbox.html'
    context_object_name = 'messages_list'

    def get_queryset(self):
        return UserMessage.objects.filter(
            user_to=self.request.user,
        )


class UserMessageFormView(LoginRequiredMixin, FormView):
    form_class = UserMessageForm

    def get_object(self):
        return self.request.user.professionalprofile

    def form_valid(self, form):
        user_message = form.cleaned_data['user_message']
        user_to_id = form.cleaned_data['user_to_id']
        company_to_id = form.cleaned_data['company_to_id']

        if user_to_id:
            user_to = User.objects.get(id=user_to_id)

            message = UserMessage.objects.create(
                user_from=self.request.user,
                user_to=user_to,
                message=user_message,
            )

            if user_to.professionalprofile.email_messages_notifications:
                subject = 'You have received a new message from {0}'.format(
                    self.request.user,
                )

                body = render_to_string(
                    'account/emails/new_private_message.html', {
                        'title': subject,
                        'message': message,
                        'base_url': settings.BASE_URL,
                    },
                )

                send_email(
                    subject=subject,
                    body=body,
                    mail_to=[user_to.email],
                )

        if company_to_id:
            company_to = Venture.objects.get(id=company_to_id)

            message = UserMessage.objects.create(
                user_from=self.request.user,
                company_to=company_to,
                message=user_message,
            )

            description = '{0} has received a new message'.format(company_to)

            # Create new message notification for company administrators.
            for membership in company_to.administratormembership_set.filter(
                status=ACTIVE_MEMBERSHIP,
                role__in=(OWNER, QJANE_ADMIN),
            ):
                user = membership.admin.user

                UserNotification.objects.create(
                    notification_type=NEW_MESSAGE_TO_COMPANY,
                    noty_to=user,
                    answered=True,
                    description=description,
                    venture_to=company_to,
                    created_by=self.request.user.professionalprofile,
                )

                if user.professionalprofile.new_company_messages_notifications:
                    subject = description

                    body = render_to_string(
                        'account/emails/new_private_message.html', {
                            'title': subject,
                            'message': message,
                            'base_url': settings.BASE_URL,
                        },
                    )

                    send_email(
                        subject=subject,
                        body=body,
                        mail_to=[user.email],
                    )

        return HttpResponse('success')


class LoadMessageModal(CustomUserMixin, View):
    def test_func(self):
        return MessagesPermissions.can_view(
            user=self.request.user,
            message=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(
            UserMessage,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        message = self.get_object()
        message.unread = False
        message.save()

        conversation = UserMessage.objects.filter(
            user_to__in=(message.user_to, message.user_from),
            user_from__in=(message.user_to, message.user_from),
        ).distinct()

        return JsonResponse(
            {
                'content': render_to_string(
                    'modals/_message_modal.html',
                    context={
                        'message': message,
                        'conversation': conversation,
                    },
                    request=self.request,
                ),
                'new_messages_counter': UserMessage.objects.filter(
                    user_to=request.user,
                    unread=True,
                ).count()
            }
        )

    def get(self, *args, **kwargs):
        raise Http404('Method not available')


class LoadConversationView(LoginRequiredMixin, View):
    def get_object(self):
        return get_object_or_404(
            User,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user_converation = self.get_object()

        conversation = UserMessage.objects.filter(
            user_to__in=(user_converation, request.user),
            user_from__in=(user_converation, request.user),
        ).distinct()

        return JsonResponse(
            {
                'content': render_to_string(
                    'modals/conversation_table.html',
                    context={
                        'conversation': conversation,
                    },
                    request=self.request,
                ),
            }
        )

    def get(self, *args, **kwargs):
        raise Http404('Method not available')


class LoadCompanyConversationView(LoginRequiredMixin, View):
    def get_object(self):
        return get_object_or_404(
            Venture,
            pk=self.kwargs['pk'],
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        company_converation = self.get_object()

        conversation = UserMessage.objects.filter(
            Q(user_from=request.user, company_to=company_converation) |
            Q(user_to=request.user, company_from=company_converation),
        ).distinct()

        return JsonResponse(
            {
                'content': render_to_string(
                    'modals/conversation_table.html',
                    context={
                        'conversation': conversation,
                    },
                    request=self.request,
                ),
            }
        )

    def get(self, *args, **kwargs):
        raise Http404('Method not available')


class LoadCustomerConversationView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            Venture,
            pk=self.kwargs['pk'],
        )

    def test_func(self):
        return EntrepreneurPermissions.can_manage_venture(
            user=self.request.user,
            venture=self.get_object()
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        company = self.get_object()
        user = User.objects.get(id=request.POST.get('user_to_id'))

        conversation = UserMessage.objects.filter(
            Q(user_from=user, company_to=company) |
            Q(user_to=user, company_from=company),
        ).distinct()

        return JsonResponse(
            {
                'content': render_to_string(
                    'modals/conversation_table.html',
                    context={
                        'conversation': conversation,
                    },
                    request=self.request,
                ),
            }
        )

    def get(self, *args, **kwargs):
        raise Http404('Method not available')
