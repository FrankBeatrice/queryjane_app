from django import template

from account.models import UserNotification

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
