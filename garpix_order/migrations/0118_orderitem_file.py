# Generated by Django 3.0.5 on 2022-01-19 21:44

from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0117_auto_20211224_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='file',
            field=models.ImageField(blank=True, null=True, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Превью'),
        ),
    ]
