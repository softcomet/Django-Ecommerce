# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-03 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0111_auto_20171203_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='sample_box_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
