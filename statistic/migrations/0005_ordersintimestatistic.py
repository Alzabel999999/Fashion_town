# Generated by Django 3.0.5 on 2021-03-25 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0004_ordersstatusstatistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdersInTimeStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Статистика по общему количеству заказов (период, фирма, логины, категории пользователей).',
            },
        ),
    ]