# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-08 11:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0014_auto_20170728_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='delivered',
            field=models.DateField(blank=True, null=True),
        ),
    ]
