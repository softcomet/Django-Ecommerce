# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-06 01:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0102_product__created_in_sprintpack'),
        ('sales', '0014_auto_20171001_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesOrderDelivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_sprintpack_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sales_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.SalesOrder')),
            ],
            options={
                'verbose_name_plural': 'Sales order deliveries',
            },
        ),
        migrations.CreateModel(
            name='SalesOrderDeliveryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Product')),
                ('sales_order_delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.SalesOrderDelivery')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='salesorderdeliveryitem',
            unique_together=set([('product', 'sales_order_delivery')]),
        ),
    ]