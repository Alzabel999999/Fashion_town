# Generated by Django 3.0.5 on 2021-11-23 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0113_auto_20211123_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
    ]
