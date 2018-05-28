from django import template
from corporative.models import LegalItem
from account.models import UserNotification
from account.data import UPDATED_TERMS
from account.data import UPDATED_PRIVACY_POLICY


register = template.Library()


@register.assignment_tag(takes_context=True)
def get_legal_item_description(context, item_slug):
    current_lan = context['request'].LANGUAGE_CODE
    item = LegalItem.objects.get(slug=item_slug)
    item_description = item.en_description

    if current_lan == 'es' and item.sp_description:
        item_description = item.sp_description

    return item_description


@register.assignment_tag(takes_context=True)
def get_answered_legal_item(context, item_slug):
    user = context['user']
    answered = True

    if item_slug == 'user-agreement':
        if UserNotification.objects.filter(
            noty_to=user,
            notification_type=UPDATED_TERMS,
            created_at__gte=user.accepted_terms_date,
        ):
            answered = False

    elif item_slug == 'privacy-policy':
        if UserNotification.objects.filter(
            noty_to=user,
            notification_type=UPDATED_PRIVACY_POLICY,
            created_at__gte=user.accepted_terms_date,
        ):
            answered = False

    return answered
