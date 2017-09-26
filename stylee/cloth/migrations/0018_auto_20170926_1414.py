# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-26 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0017_auto_20170926_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='cloth_type',
            field=models.CharField(choices=[('ts', 't-shirt'), ('ct', 'coat'), ('sh', 'shirt'), ('ja', 'jacket'), ('j', 'jean'), ('p', 'pants'), ('s', 'shoes'), ('c', 'cab')], default='1', max_length=9),
        ),
    ]