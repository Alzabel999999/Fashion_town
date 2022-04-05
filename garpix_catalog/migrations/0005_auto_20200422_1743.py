# Generated by Django 2.1 on 2020-04-22 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0004_auto_20200421_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Главная'), (2, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (5, 'Инфо')], default=3, verbose_name='Тип страницы'),
        ),
        migrations.AddField(
            model_name='product',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Главная'), (2, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (5, 'Инфо')], default=4, verbose_name='Тип страницы'),
        ),
    ]
