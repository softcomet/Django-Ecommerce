# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-11 09:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0013_auto_20171011_0940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesorder',
            old_name='paid_comission',
            new_name='paid_commission',
        ),
    ]