# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-08 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20170908_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(choices=[('ud', 'Undefined'), ('us', 'United States'), ('ko', 'South Korea'), ('jp', 'Japan'), ('ch', 'China')], default='ud', max_length=20),
        ),
    ]