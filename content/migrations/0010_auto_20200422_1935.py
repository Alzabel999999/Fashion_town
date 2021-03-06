# Generated by Django 2.1 on 2020-04-22 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_merge_20200422_1841'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['ordering'], 'verbose_name': 'Пост блога', 'verbose_name_plural': 'Посты блога'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='ordering',
            field=models.IntegerField(db_index=True, default=0, verbose_name='Порядок'),
        ),
        migrations.AlterField(
            model_name='banner',
            name='banner_type',
            field=models.CharField(choices=[('disabled', 'Не показан'), ('main_page_near_slider', 'Баннеры на главную под слайдер'), ('main_page_big', 'Большие баннеры на главную'), ('main_page_new_products', 'Баннеры для новых товаров')], default='', max_length=100, verbose_name='Тип баннера'),
        ),
    ]
