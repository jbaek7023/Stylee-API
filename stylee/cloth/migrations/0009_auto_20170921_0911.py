# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-21 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0008_auto_20170920_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=6)),
                ('brand', models.CharField(max_length=30)),
                ('size', models.CharField(max_length=12)),
                ('link', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(max_length=1)),
                ('seasons', models.CharField(max_length=1)),
                ('delivery_loc', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='wear',
            name='which',
        ),
        migrations.RemoveField(
            model_name='wear',
            name='who',
        ),
        migrations.RemoveField(
            model_name='cloth',
            name='color',
        ),
        migrations.RemoveField(
            model_name='cloth',
            name='link',
        ),
        migrations.RemoveField(
            model_name='cloth',
            name='size',
        ),
        migrations.DeleteModel(
            name='Wear',
        ),
        migrations.AddField(
            model_name='cloth',
            name='detail',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='cloth.ClothDetail'),
        ),
    ]
