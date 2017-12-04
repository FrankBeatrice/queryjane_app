#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: QJane
from django import template

from entrepreneur.models import AdministratorMembership
from entrepreneur.data import ACTIVE_MEMBERSHIP
from entrepreneur.data import SENT_INVITATION
from account.models import UserNotification
from account.data import NEW_ENTREPRENEUR_ADMIN


register = template.Library()


@register.assignment_tag
def get_user_venture_memberships(user):
    professional_profile = user.professionalprofile
    return AdministratorMembership.objects.filter(
        admin=professional_profile,
        status=ACTIVE_MEMBERSHIP,
    )


@register.assignment_tag
def get_user_venture_admin_notification(user, venture):
    if not user.is_authenticated:
        return False

    professional_profile = user.professionalprofile

    # pa_m = pending administrator membership
    pa_m = professional_profile.administratormembership_set.filter(
        venture=venture,
        status=SENT_INVITATION,
    ).first()

    return UserNotification.objects.filter(
        notification_type=NEW_ENTREPRENEUR_ADMIN,
        venture_from=venture,
        membership=pa_m,
    ).first()
