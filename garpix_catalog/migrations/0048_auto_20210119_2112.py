# Generated by Django 3.0.5 on 2021-01-19 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0047_auto_20210119_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=150, verbose_name='ЧПУ'),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=150, verbose_name='ЧПУ'),
        ),
    ]
