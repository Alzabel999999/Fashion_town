# Generated by Django 3.0.5 on 2021-05-27 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0080_auto_20210526_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Цена доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Стоимость заказа'),
        ),
        migrations.AddField(
            model_name='order',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Итоговая цена'),
        ),
    ]
