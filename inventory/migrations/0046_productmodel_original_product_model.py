# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-09 11:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0045_auto_20170709_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='original_product_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.ProductModel'),
        ),
    ]
