# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-27 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0037_pricelistsetting_price_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='pricelist',
            name='is_default',
            field=models.BooleanField(default=False, unique=True),
        ),
    ]
