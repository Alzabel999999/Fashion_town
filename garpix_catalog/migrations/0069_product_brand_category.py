# Generated by Django 3.0.5 on 2021-02-02 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0068_auto_20210201_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='brand_category_products', to='garpix_catalog.BrandCategory', verbose_name='Бренд / Категория'),
        ),
    ]
