# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-07 19:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0013_auto_20170907_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relationaddress',
            name='address_invoice',
        ),
        migrations.RemoveField(
            model_name='relationaddress',
            name='address_shipping',
        ),
    ]
