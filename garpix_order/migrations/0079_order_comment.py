# Generated by Django 3.0.5 on 2021-05-26 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0078_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Комментарий'),
        ),
    ]
