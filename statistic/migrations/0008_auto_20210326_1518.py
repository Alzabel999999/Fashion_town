# Generated by Django 3.0.5 on 2021-03-26 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistic', '0007_overageitemsinordersstatistic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='overageitemsinordersstatistic',
            options={'verbose_name': 'Статистика по среднему кол-ву товаров в посылке (без опта).'},
        ),
    ]
