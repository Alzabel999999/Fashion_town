# Generated by Django 2.1 on 2020-04-23 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0012_auto_20200423_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длина*ширина)'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длина*ширина)'),
        ),
        migrations.AlterField(
            model_name='feature',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длина*ширина)'),
        ),
        migrations.AlterField(
            model_name='sliderimage',
            name='thumb_size',
            field=models.CharField(blank=True, max_length=64, verbose_name='Размер для ресайза (формат: длина*ширина)'),
        ),
    ]
