# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-06 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0067_auto_20170825_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocklocationitem',
            name='comment',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
