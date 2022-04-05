# Generated by Django 2.0.7 on 2019-03-07 12:23

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion
import garpix_page.utils.get_file_path
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('--', '--')], default='', max_length=100, verbose_name='Позиция')),
                ('template', models.CharField(choices=[('--', '--')], default='', max_length=100, verbose_name='Шаблон')),
                ('title', models.CharField(default='', max_length=255, verbose_name='Название')),
                ('title_ru', models.CharField(default='', max_length=255, null=True, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержимое')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Содержимое')),
                ('image', models.FileField(blank=True, null=True, upload_to=garpix_page.utils.get_file_path.get_file_path, verbose_name='Изображение')),
                ('sort', models.IntegerField(default=100, help_text='Чем меньше число, тем выше будет элемент в списке.', verbose_name='Сортировка')),
            ],
            options={
                'verbose_name': 'Компонент',
                'verbose_name_plural': 'Компонент',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='ComponentChildren',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Название')),
                ('title_ru', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Название')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Текст')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Текст')),
                ('image', models.FileField(blank=True, null=True, upload_to=garpix_page.utils.get_file_path.get_file_path, verbose_name='Изображение')),
                ('sort', models.IntegerField(default=100, help_text='Чем меньше число, тем выше будет элемент в списке.', verbose_name='Сортировка')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garpix_page.Component', verbose_name='Компонент')),
            ],
            options={
                'verbose_name': 'Дочерний компонент',
                'verbose_name_plural': 'Дочерний компонент',
                'ordering': ('sort',),
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Название')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('slug', models.SlugField(blank=True, default='', max_length=150, verbose_name='ЧПУ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('seo_title', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO заголовок страницы (title)')),
                ('seo_title_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO заголовок страницы (title)')),
                ('seo_keywords', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_keywords_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO ключевые слова (keywords)')),
                ('seo_description', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO описание (description)')),
                ('seo_description_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO описание (description)')),
                ('seo_author', models.CharField(blank=True, default='', max_length=250, verbose_name='SEO автор (author)')),
                ('seo_author_ru', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SEO автор (author)')),
                ('seo_og_type', models.CharField(blank=True, default='website', max_length=250, verbose_name='SEO og:type')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержимое')),
                ('content_ru', ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Содержимое')),
                ('login_required', models.BooleanField(default=False, verbose_name='Требовать атворизацию для просмотра?')),
                ('page_type', models.IntegerField(choices=[(1, 'Главная')], default=2, verbose_name='Тип страницы')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, limit_choices_to={'page_type__gt': 1}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='garpix_page.Page', verbose_name='Родительская страница')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='component',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='garpix_page.Page', verbose_name='Страница'),
        ),
    ]