# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-13 07:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0035_relation_custom_label_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='relation',
            name='custom_label_logo',
        ),
    ]
