# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-21 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outfit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='outfit',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Undefined')], default='u', max_length=10),
        ),
    ]
