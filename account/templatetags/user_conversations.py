from django import template

from account.models import Conversation

register = template.Library()


@register.assignment_tag
def get_user_conversation(user_from, user_to):
    conversation = Conversation.objects.filter(
        participating_users__in=(user_from, user_to)
    )

    if conversation:
        return conversation[0]
    else:
        return False


@register.assignment_tag
def get_company_conversation(user, company):
    conversation = Conversation.objects.filter(
        participating_users__in=[user],
        participating_company=company,
    )

    if conversation:
        return conversation[0]
    else:
        return False
