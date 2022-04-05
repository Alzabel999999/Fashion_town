# Generated by Django 3.0.5 on 2020-12-21 15:48

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import garpix_page.utils.get_file_path
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('garpix_catalog', '0025_auto_20201217_1559'),
    ]

    operations = [
        migrations.CreateModel(
            name='LivePhotoAlbum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('slug', models.SlugField(blank=True, default='', max_length=150, verbose_name='ЧПУ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('seo_title', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO заголовок страницы (title)')),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_description', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO описание (description)')),
                ('seo_author', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO автор (author)')),
                ('seo_og_type', models.CharField(blank=True, default='website', max_length=250, verbose_name='SEO og:type')),
                ('seo_image', models.FileField(blank=True, null=True, upload_to=garpix_page.utils.get_file_path.get_file_path, verbose_name='SEO изображение')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержимое')),
                ('image', models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Изображение')),
                ('thumb_size', models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длина*ширина)')),
                ('image_thumb', models.CharField(blank=True, max_length=255)),
                ('ordering', models.IntegerField(db_index=True, default=0, verbose_name='Порядок')),
                ('sites', models.ManyToManyField(default='1', to='sites.Site', verbose_name='Сайты для отображения')),
            ],
            options={
                'verbose_name': 'Альбом живых фото',
                'verbose_name_plural': 'Альбомы живых фото',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='LivePhotoImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, default='', max_length=255, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Изображение')),
                ('thumb_size', models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длина*ширина)')),
                ('image_thumb', models.CharField(blank=True, max_length=255)),
                ('ordering', models.IntegerField(db_index=True, default=0, verbose_name='Порядок')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='live_photos', to='garpix_catalog.LivePhotoAlbum', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Живое фото',
                'verbose_name_plural': 'Живые фото',
                'ordering': ['ordering'],
            },
        ),
    ]
