# Generated by Django 3.0.5 on 2021-03-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0031_auto_20210315_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='street',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Улица'),
        ),
    ]