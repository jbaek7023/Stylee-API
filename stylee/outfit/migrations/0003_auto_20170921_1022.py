# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-21 10:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outfit', '0002_outfit_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outfit',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Unisex')], default='u', max_length=10),
        ),
    ]
