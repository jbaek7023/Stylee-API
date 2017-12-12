# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-08 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20171016_0717'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='height',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='height_in_ft',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Undefined', 'Undefined')], default='u', max_length=10),
        ),
    ]