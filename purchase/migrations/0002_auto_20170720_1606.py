# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-20 14:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0056_auto_20170715_0629'),
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('DR', 'Draft'), ('CO', 'Confirmed')], default='DR', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picking_list', models.FileField(upload_to='media/purchase/picking_list/%Y/%m/%d')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.Delivery')),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('added_to_stock', models.BooleanField(default=False)),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.Delivery')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Material')),
            ],
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('WC', 'Waiting for confirmation'), ('WA', 'Waiting delivery'), ('DL', 'Delivered')], default='DR', max_length=2),
        ),
        migrations.AlterField(
            model_name='purchaseorderitem',
            name='unit_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='delivery',
            name='purchase_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.PurchaseOrder'),
        ),
    ]
