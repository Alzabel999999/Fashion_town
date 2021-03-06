# Generated by Django 2.1 on 2020-04-21 11:50

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feature',
            name='content_ru',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', null=True, verbose_name='Содержимое'),
        ),
        migrations.AddField(
            model_name='feature',
            name='title_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
    ]
