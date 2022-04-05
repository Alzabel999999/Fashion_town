# Generated by Django 3.0.5 on 2021-01-25 16:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0009_auto_20210125_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Дополнительные данные'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Дополнительные данные'),
        ),
    ]
