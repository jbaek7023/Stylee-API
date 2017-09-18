# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-08 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_remove_profile_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='birth',
            field=models.DateField(default='1992-07-23'),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Undefined')], default='u', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(choices=[('us', 'United States'), ('ko', 'South Korea'), ('jp', 'Japan'), ('ch', 'China')], default='us', max_length=20),
        ),
    ]