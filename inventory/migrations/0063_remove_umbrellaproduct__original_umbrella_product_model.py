# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-27 06:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0062_umbrellaproduct__original_umbrella_product_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='umbrellaproduct',
            name='_original_umbrella_product_model',
        ),
    ]
