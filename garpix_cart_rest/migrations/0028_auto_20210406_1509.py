# Generated by Django 3.0.5 on 2021-04-06 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0105_auto_20210405_1519'),
        ('garpix_cart_rest', '0027_auto_20210403_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sku_cart_items', to='garpix_catalog.ProductSku', verbose_name='Продукт'),
            preserve_default=False,
        ),
    ]