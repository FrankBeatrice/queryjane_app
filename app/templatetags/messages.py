from django import template

from account.models import UserMessage
from account.models import Conversation

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
def get_recent_user_conversations(user):
    return Conversation.objects.filter(
        participating_users__in=[user],
    )[:10]
