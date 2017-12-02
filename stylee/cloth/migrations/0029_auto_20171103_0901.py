# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-03 09:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0028_auto_20171102_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='big_cloth_type',
            field=models.CharField(blank=True, choices=[('t', 'Top'), ('b', 'Bottom'), ('o', 'Outwear'), ('s', 'Shoes'), ('e', 'ETC')], default='t', max_length=11, null=True),
        ),
        migrations.AlterField(
            model_name='cloth',
            name='cloth_type',
            field=models.CharField(blank=True, choices=[('ts', 't-shirt'), ('ct', 'coat'), ('sh', 'shirt'), ('ja', 'jacket'), ('j', 'jean'), ('p', 'pants'), ('s', 'shoes'), ('c', 'cab')], default='1', max_length=9, null=True),
        ),
    ]