# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-17 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0117_auto_20180118_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='umbrellaproductmodel',
            name='product_type',
            field=models.CharField(blank=True, choices=[('PL', 'Blanket'), ('BA', 'Basket'), ('CA', 'Carrier'), ('JA', 'Jacket'), ('SW', 'Sweater'), ('CU', 'Cushion'), ('PB', 'Poop Bag'), ('HA', 'Handbag'), ('TW', 'Table Ware'), ('BE', 'Beach Items')], max_length=2, null=True),
        ),
    ]