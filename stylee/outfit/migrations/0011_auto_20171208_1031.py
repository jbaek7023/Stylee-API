# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-08 10:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outfit', '0010_auto_20171208_1020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outfit',
            old_name='publish',
            new_name='created_at',
        ),
    ]