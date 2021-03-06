# Generated by Django 3.0.5 on 2021-04-15 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0065_auto_20210414_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='fixed_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Фиксированная цена'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена'),
        ),
    ]
