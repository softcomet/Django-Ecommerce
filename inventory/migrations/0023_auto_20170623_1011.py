# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-23 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_auto_20170622_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
