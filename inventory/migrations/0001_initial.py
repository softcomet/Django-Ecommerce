# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-01 15:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=50)),
                ('sku_supplier', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('mat_type', models.CharField(choices=[('TIM', 'Time'), ('FAB', 'Fabric'), ('ACC', 'Accesories'), ('FIL', 'Filling'), ('SMA', 'Small Materials')], max_length=3)),
                ('quantity_in_stock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('sku', models.CharField(max_length=50)),
                ('materials', models.ManyToManyField(to='inventory.Material')),
            ],
        ),
    ]
