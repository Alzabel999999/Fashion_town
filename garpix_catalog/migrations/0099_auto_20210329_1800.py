# Generated by Django 3.0.5 on 2021-03-29 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0098_auto_20210323_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
    ]
