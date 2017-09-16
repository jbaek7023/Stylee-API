# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-16 11:50
from __future__ import unicode_literals

from django.db import migrations, models
import outfit.models


class Migration(migrations.Migration):

    dependencies = [
        ('outfit', '0004_auto_20170915_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='location',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='outfit',
            name='outfit_img',
            field=models.ImageField(blank=True, null=True, upload_to=outfit.models.upload_location),
        ),
    ]
