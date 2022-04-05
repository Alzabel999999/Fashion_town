# Generated by Django 3.0.5 on 2021-01-14 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0041_auto_20210114_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='title',
            field=models.CharField(choices=[('RUB', 'Российский рубль'), ('BYN', 'Белорусский рубль'), ('UAH', 'Украинская гривна'), ('KZT', 'Казахстанский тенге'), ('USD', 'Американский доллар'), ('EUR', 'Евро')], default='RUB', max_length=3, unique=True, verbose_name='Валюта'),
        ),
    ]