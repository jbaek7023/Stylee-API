# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-28 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0012_auto_20170928_0438'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
        migrations.AddField(
            model_name='profile',
            name='height',
            field=models.CharField(default='undefined', max_length=5),
        ),
        migrations.AddField(
            model_name='profile',
            name='height_in_ft',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.TextField(blank=True, max_length=155),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('u', 'Not Specified')], default='u', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(choices=[('ud', 'Not Specified'), ('us', 'United States'), ('ko', 'South Korea'), ('jp', 'Japan'), ('ch', 'China')], default='ud', max_length=40),
        ),
    ]
