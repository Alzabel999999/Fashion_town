# Generated by Django 3.0.5 on 2021-05-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0073_auto_20210520_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment_passport',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Комментарий ПД'),
        ),
        migrations.AddField(
            model_name='order',
            name='wait_call',
            field=models.BooleanField(default=False, verbose_name='Дождаться звонка'),
        ),
    ]
