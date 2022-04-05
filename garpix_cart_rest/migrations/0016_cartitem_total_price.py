# Generated by Django 3.0.5 on 2021-04-01 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0015_cartitem_selected'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Итоговая цена'),
        ),
    ]