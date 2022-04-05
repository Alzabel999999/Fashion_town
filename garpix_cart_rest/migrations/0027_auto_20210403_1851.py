# Generated by Django 3.0.5 on 2021-04-03 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0103_remove_productsku_sku_rc'),
        ('garpix_cart_rest', '0026_cartitemspack_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemspack',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_catalog.Size', verbose_name='Размер'),
        ),
        migrations.AlterField(
            model_name='cartitemspack',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_catalog.Color', verbose_name='Цвет'),
        ),
    ]
