# Generated by Django 2.1 on 2020-04-23 16:33

from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0005_auto_20200422_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='content',
            field=models.TextField(blank=True, default='', verbose_name='Содержимое'),
        ),
    ]
