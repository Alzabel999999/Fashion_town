# Generated by Django 3.0.5 on 2021-01-22 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0006_auto_20210119_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondenceitem',
            name='message',
            field=models.TextField(blank=True, default='', verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='address',
            field=models.CharField(default='', max_length=255, verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='title',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='requisites',
            name='requisites',
            field=models.TextField(blank=True, default='', max_length=400, verbose_name='Реквизиты'),
        ),
    ]
