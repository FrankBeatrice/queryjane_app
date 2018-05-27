# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-26 22:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0031_auto_20180512_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='accepted_terms',
            field=models.BooleanField(default=True, verbose_name='accepted terms and conditions'),
        ),
        migrations.AddField(
            model_name='user',
            name='accepted_terms_date',
            field=models.DateField(blank=True, null=True, verbose_name='accepted terms and conditions date'),
        ),
    ]
