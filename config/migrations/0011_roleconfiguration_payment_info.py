# Generated by Django 3.0.5 on 2021-04-01 16:27

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0010_remove_siteconfiguration_delivery_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='roleconfiguration',
            name='payment_info',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, default='', verbose_name='Оплата'),
        ),
    ]
