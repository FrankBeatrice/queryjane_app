# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-22 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_usernotification_job_offer'),
        ('entrepreneur', '0009_auto_20180112_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.ProfessionalProfile', verbose_name='applicant')),
                ('job_offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entrepreneur.JobOffer', verbose_name='job offer')),
            ],
            options={
                'verbose_name': 'applicant',
                'verbose_name_plural': 'applicants',
                'ordering': ('-created_at',),
            },
        ),
    ]