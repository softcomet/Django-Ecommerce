# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-11 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_auto_20170910_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='_xero_invoice_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
