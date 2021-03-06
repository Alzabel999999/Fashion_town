# Generated by Django 3.0.5 on 2021-06-09 10:19

from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20210607_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopconfig',
            name='info_delivery_photo',
            field=models.FileField(blank=True, default='', upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Информация о доставке (фото)'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='info_exchange_photo',
            field=models.FileField(blank=True, default='', upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Информация о возврате и обмене (фото)'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='info_juridical_photo',
            field=models.FileField(blank=True, default='', upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Юридическая информация (фото)'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='info_payment_photo',
            field=models.FileField(blank=True, default='', upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Информация об оплате (фото)'),
        ),
    ]
