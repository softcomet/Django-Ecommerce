# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-08 08:15
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0072_material_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
