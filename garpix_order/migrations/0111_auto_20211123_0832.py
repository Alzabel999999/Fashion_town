# Generated by Django 3.0.5 on 2021-11-23 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0110_auto_20211123_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='type',
            field=models.CharField(choices=[('online', 'Онлайн'), ('balance', 'Списание с баланса')], max_length=100, verbose_name='Тип оплаты'),
        ),
    ]
