# Generated by Django 3.0.5 on 2021-03-31 11:40

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0013_auto_20210312_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='comment',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Комментарий'),
        ),
    ]
