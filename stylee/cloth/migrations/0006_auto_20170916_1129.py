# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-16 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0005_auto_20170915_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='link',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]