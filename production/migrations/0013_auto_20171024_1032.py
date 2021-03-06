# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-24 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0012_auto_20171013_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productionorder',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('WC', 'Waiting for confirmation'), ('WA', 'Waiting delivery'), ('PD', 'Partially Delivered'), ('DL', 'Delivered'), ('IN', 'Invoice added')], default='DR', max_length=2),
        ),
    ]
