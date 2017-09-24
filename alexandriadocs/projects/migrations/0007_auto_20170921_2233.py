# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 22:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0006_auto_20170921_2218'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='projectcollaborator',
            index_together=set([('user', 'project')]),
        ),
    ]
