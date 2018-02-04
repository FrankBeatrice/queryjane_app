from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import ListView
from django.views.generic import View

from account.models import UserNotification
from account.permissions import NotificationPermissions
from app.mixins import CustomUserMixin
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import REJECTED_MEMBERSHIP
from entrepreneur.data import SENT_INVITATION


class NotificationsView(LoginRequiredMixin, ListView):
    model = UserNotification
    template_name = 'account/notifications.html'
    context_object_name = 'notifications_list'

    def get_queryset(self):
        return UserNotification.objects.filter(
            noty_to=self.request.user,
        )


class LoadNotificationModal(CustomUserMixin, View):
    def test_func(self):
        return NotificationPermissions.can_view(
            user=self.request.user,
            notification=self.get_object(),
        )

    def get_object(self):
        return get_object_or_404(
            UserNotification, id=self.kwargs.get('pk'),
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.was_seen = True
        notification.save()

        return JsonResponse({'content': render_to_string(
            'modals/_notification_modal.html',
            context={
                'notification': notification,
            },
            request=self.request,
        )})

    def get(self, *args, **kwargs):
        raise Http404('Method not available')


class AdminNotificationAcceptView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            UserNotification,
            pk=self.kwargs['pk'],
        )

    def test_func(self):
        return NotificationPermissions.can_answer_admin_invitation(
            user=self.request.user,
            venture=self.get_object().venture_from
        )

    def get(self, *args, **kwargs):
        notification = self.get_object()

        notification.answered = True
        notification.save()

        membership = notification.membership
        membership.status = ACTIVE_MEMBERSHIP
        membership.save()

        return redirect(
            'entrepreneur:settings_venture_form',
            notification.venture_from.slug,
        )


class AdminNotificationRejectView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            UserNotification,
            pk=self.kwargs['pk'],
        )

    def test_func(self):
        return NotificationPermissions.can_answer_admin_invitation(
            user=self.request.user,
            venture=self.get_object().venture_from
        )

    def get(self, *args, **kwargs):
        notification = self.get_object()

        notification.answered = True
        notification.save()

        membership = notification.membership
        membership.status = REJECTED_MEMBERSHIP
        membership.save()

        return redirect(
            'venture_detail',
            notification.venture_from.slug,
        )


class AdminNotificationResendView(CustomUserMixin, View):
    def get_object(self):
        return get_object_or_404(
            UserNotification, id=self.kwargs.get('pk'),
        )

    def test_func(self):
        return NotificationPermissions.can_resend_admin_invitation(
            user=self.request.user,
            venture=self.get_object().venture_from
        )

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.was_seen = False
        notification.answered = False
        notification.created_at = timezone.now()
        notification.created_by = request.user.professionalprofile
        notification.save()

        membership = notification.membership
        membership.status = SENT_INVITATION
        membership.created_by = request.user.professionalprofile
        membership.created_at = timezone.now()
        membership.save()

        return JsonResponse({'content': render_to_string(
            'entrepreneur/venture_settings/_membership_line.html',
            context={
                'membership': membership,
            },
            request=self.request,
        )})

    def get(self, *args, **kwargs):
        raise Http404('Method not available')
