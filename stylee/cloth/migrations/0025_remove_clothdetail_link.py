# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-18 08:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0024_cloth_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clothdetail',
            name='link',
        ),
    ]