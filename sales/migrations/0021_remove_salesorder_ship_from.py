# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-25 06:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0020_auto_20171024_1121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesorder',
            name='ship_from',
        ),
    ]
