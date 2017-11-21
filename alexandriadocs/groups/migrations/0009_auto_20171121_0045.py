# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 00:45
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0008_auto_20170921_2233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['name', 'created'], 'verbose_name': 'group'},
        ),
        migrations.RenameField(
            model_name='group',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, editable=False, populate_from='name', verbose_name='slug'),
        ),
    ]
