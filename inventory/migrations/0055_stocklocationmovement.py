# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-15 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0054_auto_20170712_0009'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockLocationMovement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty_change', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Material')),
                ('stock_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.StockLocation')),
            ],
        ),
    ]
