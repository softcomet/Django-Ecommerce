# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-03 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0030_merge_20171011_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
