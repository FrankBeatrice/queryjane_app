#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Angel App
from __future__ import unicode_literals
from django_countries.fields import CountryField

from django.db import models


class City(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='name',
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        verbose_name='state',
    )

    country = models.ForeignKey(
        'place.Country',
        verbose_name='country',
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = 'city'
        verbose_name_plural = 'cities'


class State(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='name',
    )

    country = models.ForeignKey(
        'place.Country',
        verbose_name='country',
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = 'state'
        verbose_name_plural = 'states'


class Country(models.Model):
    country = CountryField(
        unique=True,
    )

    name = models.CharField(
        max_length=100,
        verbose_name='name',
    )

    def __str__(self):
        return '{0}'.format(self.country.name)

    class Meta:
        ordering = ('country',)
        verbose_name = 'country'
        verbose_name_plural = 'countries'
