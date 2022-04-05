# Generated by Django 3.0.5 on 2021-04-01 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0102_brand_sertificate'),
        ('garpix_cart_rest', '0019_auto_20210401_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sku_cart_items', to='garpix_catalog.ProductSku', verbose_name='Продукт'),
        ),
    ]
