from django.utils import timezone
from datetime import time

from django import template

register = template.Library()


@register.assignment_tag
def get_general_greeting():
    # Good morning
    morning_init = time(4, 20, 0)
    morning_end = time(12, 00, 0)
    afternoon_init = time(12, 00, 0)
    afternoon_end = time(18, 30, 0)

    now = timezone.now()
    current_time = now.time()
    general_greeting = 'Good evening'

    if current_time > morning_init and current_time < morning_end:
        general_greeting = 'Good morning'
    if current_time > afternoon_init and current_time < afternoon_end:
        general_greeting = 'Good afternoon'

    return general_greeting
