# Generated by Django 3.0.5 on 2021-01-27 13:27

import ckeditor_uploader.fields
from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0020_banner_footnote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержимое')),
                ('url', models.CharField(blank=True, default='/', max_length=1000, verbose_name='URL')),
                ('target_blank', models.BooleanField(default=False, verbose_name='Открывать в новом окне')),
                ('background', models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Фон')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
            ],
            options={
                'verbose_name': 'Анонс',
                'verbose_name_plural': 'Анонсы',
            },
        ),
    ]