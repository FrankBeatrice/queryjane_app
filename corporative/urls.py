#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: QJane
from django.conf.urls import url

from .views import CorporativeInfoDetail


urlpatterns = [
    url(
        r'^(?P<slug>[-\w]+)/$',
        CorporativeInfoDetail.as_view(),
        name='corporative_detail',
    ),
]
