# Generated by Django 3.0.5 on 2021-03-11 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0024_auto_20210311_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='title',
        ),
    ]
