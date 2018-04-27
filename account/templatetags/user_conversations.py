import functools

from django import template

from account.models import Conversation

register = template.Library()


@register.assignment_tag
def get_user_conversation(user_from, user_to):
    conversation_list = functools.reduce(
        lambda qs, pk: qs.filter(participating_users=pk),
        [user_from, user_to],
        Conversation.objects.all()
    )

    if conversation_list:
        return conversation_list[0]
    else:
        return False


@register.assignment_tag
def get_company_conversation(user, company):
    conversation_list = functools.reduce(
        lambda qs, pk: qs.filter(participating_users=pk),
        [user],
        Conversation.objects.filter(
            participating_company_id=company.id,
        ),
    )

    if conversation_list:
        return conversation_list[0]
    else:
        return False
