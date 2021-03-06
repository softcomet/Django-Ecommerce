# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-11 19:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0048_auto_20170711_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ean_code', models.CharField(blank=True, max_length=13, null=True)),
                ('active', models.BooleanField(default=True)),
                ('complete', models.BooleanField(default=False)),
                ('sku', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductBillOfMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_needed', models.FloatField()),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Material')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Product')),
            ],
            options={
                'ordering': ('material__supplier', 'material', 'product'),
            },
        ),
        migrations.CreateModel(
            name='UmbrellaProductModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.CharField(max_length=10)),
                ('all_patterns_present', models.BooleanField(default=False)),
                ('product_images_present', models.BooleanField(default=False)),
                ('product_type', models.CharField(blank=True, choices=[('PL', 'Plaid'), ('BA', 'Basket'), ('CA', 'Carrier'), ('JA', 'Jacket'), ('SW', 'Sweater'), ('CU', 'Cushion')], max_length=2, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('original_umbrella_product_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.UmbrellaProductModel')),
            ],
        ),
        migrations.CreateModel(
            name='UmbrellaProductModelImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to='media/umbrella_product_model/images/%Y/%m/%d')),
                ('umbrella_product_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.UmbrellaProductModel')),
            ],
        ),
        migrations.CreateModel(
            name='UmbrellaProductModelProductionDescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Step name')),
                ('description', models.TextField(verbose_name='What to do and how to do it')),
                ('image', models.FileField(blank=True, null=True, upload_to='media/umbrella_product_models/production_description/images/%Y/%m/%d')),
                ('umbrella_product_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.UmbrellaProductModel')),
            ],
        ),
        migrations.RemoveField(
            model_name='productmodelimage',
            name='product_model',
        ),
        migrations.RemoveField(
            model_name='productmodelproductiondescription',
            name='product_model',
        ),
        migrations.AlterModelOptions(
            name='umbrellaproductbillofmaterial',
            options={'ordering': ('material__supplier', 'material', 'umbrella_product')},
        ),
        migrations.RenameField(
            model_name='umbrellaproductbillofmaterial',
            old_name='product',
            new_name='umbrella_product',
        ),
        migrations.RemoveField(
            model_name='umbrellaproduct',
            name='ean_code',
        ),
        migrations.RemoveField(
            model_name='umbrellaproduct',
            name='model',
        ),
        migrations.AlterField(
            model_name='productmodelpattern',
            name='pattern_image',
            field=models.FileField(upload_to='media/product_model/patterns/image/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='productmodelpattern',
            name='pattern_vector',
            field=models.FileField(upload_to='media/product_model/patterns/vector/%Y/%m/%d'),
        ),
        migrations.AlterUniqueTogether(
            name='productmodel',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='umbrellaproductbillofmaterial',
            unique_together=set([('material', 'umbrella_product')]),
        ),
        migrations.DeleteModel(
            name='ProductModelImage',
        ),
        migrations.DeleteModel(
            name='ProductModelProductionDescription',
        ),
        migrations.AddField(
            model_name='product',
            name='product_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.ProductModel'),
        ),
        migrations.AddField(
            model_name='product',
            name='umbrella_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.UmbrellaProduct'),
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='all_patterns_present',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='description',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='name',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='number',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='original_product_model',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='product_images_present',
        ),
        migrations.RemoveField(
            model_name='productmodel',
            name='product_type',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='umbrella_product_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.UmbrellaProductModel'),
        ),
        migrations.AddField(
            model_name='umbrellaproduct',
            name='umbrella_product_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.UmbrellaProductModel'),
        ),
        migrations.AlterUniqueTogether(
            name='productbillofmaterial',
            unique_together=set([('material', 'product')]),
        ),
    ]
