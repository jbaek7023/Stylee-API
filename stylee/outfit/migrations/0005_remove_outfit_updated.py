# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-29 16:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outfit', '0004_outfit_only_me'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='outfit',
            name='updated',
        ),
    ]
