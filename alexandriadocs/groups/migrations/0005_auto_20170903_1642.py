# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-03 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_group_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['title', 'created'], 'verbose_name': 'group'},
        ),
        migrations.AlterField(
            model_name='group',
            name='description',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='group',
            name='title',
            field=models.CharField(max_length=128, verbose_name='title'),
        ),
    ]