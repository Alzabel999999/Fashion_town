# Generated by Django 3.0.5 on 2021-03-10 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0011_auto_20210310_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='slug',
        ),
    ]
