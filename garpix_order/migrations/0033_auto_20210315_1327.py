# Generated by Django 3.0.5 on 2021-03-15 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0032_auto_20210315_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='order',
            name='middle_name',
            field=models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='Отчество'),
        ),
    ]
