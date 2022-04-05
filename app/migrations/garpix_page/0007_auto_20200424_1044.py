# Generated by Django 2.1 on 2020-04-24 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0006_auto_20200422_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Главная'), (2, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (5, 'Инфо'), (6, 'Авторизация'), (7, 'Регистрация'), (8, 'ЛК'), (9, 'Корзина'), (15, 'Поиск')], default=2, verbose_name='Тип страницы'),
        ),
    ]