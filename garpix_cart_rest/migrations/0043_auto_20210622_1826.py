# Generated by Django 3.0.5 on 2021-06-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0042_auto_20210621_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='selected',
            field=models.BooleanField(default=True, verbose_name='Выбрано'),
        ),
        migrations.AlterField(
            model_name='cartitemspack',
            name='selected',
            field=models.BooleanField(default=True, verbose_name='Выбрано'),
        ),
    ]