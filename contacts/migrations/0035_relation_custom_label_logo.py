# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-13 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0034_auto_20171210_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='relation',
            name='custom_label_logo',
            field=models.ImageField(blank=True, null=True, upload_to='media/relation/custom_label_logo/%Y/%m/%d'),
        ),
    ]