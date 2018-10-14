#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: QJane
from django.conf.urls import url

from .views import CitySearch
from .views import CountrySearch
from .views import CityCreate
from .views import CountryFlag


urlpatterns = [
    url(
        r'^country-search/$',
        CountrySearch.as_view(),
        name='country_search',
    ),

    # API City-Serch
    url(
        r'^city-search/$',
        CitySearch.as_view(),
        name='city_search',
    ),

    url(
        r'^ax-city-create/$',
        CityCreate.as_view(),
        name='ax_city_create',
    ),

    url(
        r'^ax-country-flag/$',
        CountryFlag.as_view(),
        name='country_flag',
    ),
]
