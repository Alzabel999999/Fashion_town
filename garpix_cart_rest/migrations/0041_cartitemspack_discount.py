# Generated by Django 3.0.5 on 2021-05-27 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0040_auto_20210519_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitemspack',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True, verbose_name='Скидка'),
        ),
    ]