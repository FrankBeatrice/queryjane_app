from django import template

from account.models import UserNotification
from account.data import UPDATED_TERMS
from account.data import UPDATED_PRIVACY_POLICY

register = template.Library()


@register.assignment_tag
def get_user_notifications_count(user):
    return UserNotification.objects.filter(
        noty_to=user,
    ).count()


@register.assignment_tag
def get_new_user_notifications_count(user):
    return UserNotification.objects.filter(
        was_seen=False,
        noty_to=user,
    ).count()


@register.assignment_tag
def get_recent_user_notifications(user):
    return UserNotification.objects.filter(
        noty_to=user,
    )[:10]


@register.assignment_tag
def get_unanswered_user_agreement_notification(user):
    return UserNotification.objects.filter(
        noty_to=user,
        notification_type=UPDATED_TERMS,
        created_at__gte=user.accepted_terms_date,
    )


@register.assignment_tag
def get_unanswered_privacy_policy_notification(user):
    return UserNotification.objects.filter(
        noty_to=user,
        notification_type=UPDATED_PRIVACY_POLICY,
        created_at__gte=user.accepted_terms_date,
    )
