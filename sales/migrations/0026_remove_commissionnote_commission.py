# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-03 09:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0025_auto_20171103_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commissionnote',
            name='commission',
        ),
    ]
