# Generated by Django 3.0.5 on 2021-01-22 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0055_auto_20210122_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='redemptioncondition',
            name='is_min_for_model',
        ),
        migrations.RemoveField(
            model_name='redemptioncondition',
            name='order_type',
        ),
    ]
