# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-23 19:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0029_auto_20170623_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='product_type',
            field=models.CharField(blank=True, choices=[('PL', 'Plaid'), ('BA', 'Basket'), ('CA', 'Carrier'), ('JA', 'Jacket'), ('SW', 'Sweater'), ('CU', 'Cushion')], max_length=2, null=True),
        ),
    ]
