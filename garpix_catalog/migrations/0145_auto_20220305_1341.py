# Generated by Django 3.0.5 on 2022-03-05 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0144_product_vendor_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='vendor_code',
            field=models.CharField(blank=True, default='A', max_length=255, verbose_name='Артикул'),
        ),
    ]