# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-21 10:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0011_auto_20170921_1022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cloth',
            name='detail',
        ),
        migrations.AddField(
            model_name='clothdetail',
            name='cloth',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloth.Cloth'),
        ),
    ]
