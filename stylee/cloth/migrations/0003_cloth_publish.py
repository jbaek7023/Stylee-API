# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-15 11:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0002_remove_cloth_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloth',
            name='publish',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
