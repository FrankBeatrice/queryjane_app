from django import template

from account.models import UserMessage

register = template.Library()


@register.assignment_tag
def get_user_messages_count(user):
    return UserMessage.objects.filter(
        user_to=user,
    ).count()


@register.assignment_tag
def get_new_user_messages_count(user):
    return UserMessage.objects.filter(
        unread=True,
        user_to=user,
    ).count()


@register.assignment_tag
def get_recent_user_messages(user):
    return UserMessage.objects.filter(
        user_to=user,
    )[:10]
