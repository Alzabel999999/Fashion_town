# Generated by Django 3.0.5 on 2021-01-20 16:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0050_auto_20210120_1215'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livephotofeedback',
            options={'verbose_name': 'Запрос с живых фото', 'verbose_name_plural': 'Запросы с живых фото'},
        ),
        migrations.AddField(
            model_name='livephotofeedback',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 20, 16, 6, 41, 9372), verbose_name='Создано'),
        ),
    ]
