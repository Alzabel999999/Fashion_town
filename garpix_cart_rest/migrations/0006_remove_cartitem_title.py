# Generated by Django 3.0.5 on 2021-01-26 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0005_auto_20210125_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='title',
        ),
    ]