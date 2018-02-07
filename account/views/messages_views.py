from django.conf import settings

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.generic import FormView
from django.views.generic import View

from account.models import User
from account.models import UserMessage
from account.permissions import MessagesPermissions
from app.mixins import CustomUserMixin
from app.tasks import send_email
from account.forms import UserMessageForm


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

        user_to = User.objects.get(id=user_to_id)

        message = UserMessage.objects.create(
            user_from=self.request.user,
            user_to=user_to,
            message=user_message,
        )

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

        return JsonResponse(
            {
                'content': render_to_string(
                    'modals/_message_modal.html',
                    context={
                        'message': message,
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
