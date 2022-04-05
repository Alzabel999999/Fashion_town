# Generated by Django 2.1 on 2020-04-24 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0011_product_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Главная'), (2, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (5, 'Инфо'), (6, 'Авторизация'), (7, 'Регистрация'), (8, 'ЛК'), (9, 'Корзина'), (15, 'Поиск')], default=3, verbose_name='Тип страницы'),
        ),
        migrations.AlterField(
            model_name='product',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Главная'), (2, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (5, 'Инфо'), (6, 'Авторизация'), (7, 'Регистрация'), (8, 'ЛК'), (9, 'Корзина'), (15, 'Поиск')], default=4, verbose_name='Тип страницы'),
        ),
    ]
