# Generated by Django 3.0.5 on 2021-02-17 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0020_auto_20210217_1211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentmethod',
            options={'verbose_name': 'Метод оплаты', 'verbose_name_plural': 'Методы оплаты'},
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='content',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='image',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='image_thumb',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='ordering',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='thumb_size',
        ),
        migrations.RemoveField(
            model_name='paymentmethod',
            name='updated_at',
        ),
    ]
