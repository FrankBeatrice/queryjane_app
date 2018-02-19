#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: QJane
from django.conf.urls import url
from django.views.generic import TemplateView

urlpatterns = [
    url(
        r'^user-agreement/$',
        TemplateView.as_view(template_name='corporative/user_agreement.html'),
        name='user_agreement',
    ),

    url(
        r'^privacy-policy/$',
        TemplateView.as_view(template_name='corporative/privacy_policy.html'),
        name='privacy_policy',
    ),
]
