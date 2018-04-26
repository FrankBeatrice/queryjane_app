from django import template

from account.models import Conversation

register = template.Library()


@register.assignment_tag
def get_user_conversation(user_from, user_to):
    return Conversation.objects.filter(
        participating_users__in=(user_from, user_to)
    )[0]
