# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-08 10:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0033_auto_20171208_0935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cloth',
            old_name='created_at',
            new_name='publish',
        ),
    ]
