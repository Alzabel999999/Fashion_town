# Generated by Django 2.1 on 2020-04-21 13:21

import ckeditor_uploader.fields
from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20200421_1150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Изображение')),
                ('ordering', models.IntegerField(db_index=True, default=0, verbose_name='Порядок')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержимое')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Содержимое')),
                ('url', models.CharField(blank=True, max_length=1000, null=True, verbose_name='URL')),
                ('target_blank', models.BooleanField(default=False, verbose_name='Открывать в новом окне')),
                ('css_class', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Дополнительный класс CSS')),
                ('banner_type', models.CharField(choices=[('disabled', 'Not shown'), ('main_page', 'Main page')], default='', max_length=100, verbose_name='Тип баннера')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['ordering'],
            },
        ),
    ]
