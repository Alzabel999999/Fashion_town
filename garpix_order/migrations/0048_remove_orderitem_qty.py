# Generated by Django 3.0.5 on 2021-03-31 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0047_orderitem_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='qty',
        ),
    ]
