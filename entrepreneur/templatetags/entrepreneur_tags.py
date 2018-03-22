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


@register.assignment_tag
def get_company_logo_extension(logo_str):
    return logo_str.split('.')[-1]


@register.assignment_tag(takes_context=True)
def get_company_description(context, company):
    current_lan = context['request'].LANGUAGE_CODE
    company_description = company.description_en

    if current_lan == 'es' and company.description_es:
        company_description = company.description_es

    return company_description


@register.assignment_tag(takes_context=True)
def get_profile_description(context, profile):
    current_lan = context['request'].LANGUAGE_CODE
    profile_description = profile.description_en

    if current_lan == 'es' and profile.description_es:
        profile_description = profile.description_es

    return profile_description
