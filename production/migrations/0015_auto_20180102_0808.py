# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-01-02 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0014_auto_20171101_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionorderdelivery',
            name='carrier',
            field=models.CharField(max_length=20),
        ),
    ]
