# Generated by Django 3.0.5 on 2021-12-24 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0116_auto_20211123_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='delivery_price',
            field=models.PositiveIntegerField(verbose_name='Цена доставки для розницы'),
        ),
    ]
