# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-20 05:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import outfit.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cloth', '0006_auto_20170916_1129'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=30)),
                ('publish', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('outfit_img', models.ImageField(blank=True, null=True, upload_to=outfit.models.upload_location_outfit)),
                ('location', models.CharField(blank=True, max_length=20, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='outfit.Outfit')),
                ('tagged_clothes', models.ManyToManyField(blank=True, to='cloth.Cloth')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
