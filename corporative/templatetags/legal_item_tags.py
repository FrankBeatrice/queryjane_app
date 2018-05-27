from django import template

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_legal_item_description(context, item):
    current_lan = context['request'].LANGUAGE_CODE
    item_description = item.en_description

    if current_lan == 'es' and item.sp_description:
        item_description = item.sp_description

    return item_description
