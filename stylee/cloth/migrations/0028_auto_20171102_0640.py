# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-02 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0027_auto_20171102_0625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='content',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]