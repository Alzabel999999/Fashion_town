# Generated by Django 3.0.5 on 2021-05-31 15:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0083_auto_20210531_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='correspondenceitem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]
