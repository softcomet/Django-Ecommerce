# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-09 07:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricelists', '0003_auto_20171209_0800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricelist',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='pricelistitem',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='pricetransport',
            options={'managed': False},
        ),
    ]
