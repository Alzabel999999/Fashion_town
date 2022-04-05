# Generated by Django 3.0.5 on 2020-12-29 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0033_productsku_orders_count'),
        ('garpix_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_catalog.ProductSku', verbose_name='Продукт'),
        ),
    ]
