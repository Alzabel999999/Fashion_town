# Generated by Django 3.0.5 on 2021-05-13 11:55

from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0013_siteconfiguration_page_type_shop_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfiguration',
            name='order_condition',
            field=models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Условия оформления заказа'),
        ),
        migrations.AddField(
            model_name='siteconfiguration',
            name='return_rules',
            field=models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Правила возврата'),
        ),
    ]
