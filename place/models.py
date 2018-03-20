from __future__ import unicode_literals
from django.utils.translation import ugettext as _
from django_countries.fields import CountryField

from django.db import models


class City(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )

    state = models.ForeignKey(
        'place.State',
        null=True,
        verbose_name=_('state'),
    )

    country = models.ForeignKey(
        'place.Country',
        verbose_name=_('country'),
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class State(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )

    country = models.ForeignKey(
        'place.Country',
        verbose_name=_('country'),
    )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering = ('name',)
        verbose_name = _('state')
        verbose_name_plural = _('states')


class Country(models.Model):
    country = CountryField(
        unique=True,
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
    )

    @property
    def flag(self):
        return '/static/img/flags/{}.png'.format(self.country.code.lower())

    def __str__(self):
        return '{0}'.format(self.country.name)

    class Meta:
        ordering = ('country',)
        verbose_name = _('country')
        verbose_name_plural = _('countries')
