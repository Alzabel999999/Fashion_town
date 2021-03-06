# Generated by Django 2.1 on 2020-04-23 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0008_auto_20200423_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_thumb',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='category',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длинахширина)'),
        ),
        migrations.AddField(
            model_name='producer',
            name='image_thumb',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='producer',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длинахширина)'),
        ),
        migrations.AddField(
            model_name='product',
            name='image_thumb',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='product',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длинахширина)'),
        ),
        migrations.AddField(
            model_name='productimage',
            name='image_thumb',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='productimage',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длинахширина)'),
        ),
    ]
