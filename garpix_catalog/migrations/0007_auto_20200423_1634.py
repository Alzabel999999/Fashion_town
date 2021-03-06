# Generated by Django 2.1 on 2020-04-23 16:34

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0006_auto_20200423_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_content',
            field=models.TextField(blank=True, default='', verbose_name='Содержимое'),
        ),
        migrations.AlterField(
            model_name='product',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Содержимое'),
        ),
    ]
