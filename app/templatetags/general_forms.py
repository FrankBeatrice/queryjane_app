from django import template

from account.forms import UserMessageForm


register = template.Library()


@register.assignment_tag
def get_message_form():
    return UserMessageForm()
