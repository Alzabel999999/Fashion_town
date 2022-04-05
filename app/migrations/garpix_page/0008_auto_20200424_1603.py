# Generated by Django 2.1 on 2020-04-24 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_page', '0007_auto_20200424_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='page_type',
            field=models.IntegerField(choices=[(1, 'Главная'), (2, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (5, 'Инфо'), (6, 'Авторизация'), (7, 'Регистрация'), (8, 'ЛК'), (9, 'Корзина'), (10, 'Вспомнить пароль'), (11, 'Оформление заказа'), (12, 'История заказов'), (13, 'Избранное (вишлист)'), (14, 'Сравнение'), (15, 'Поиск')], default=2, verbose_name='Тип страницы'),
        ),
    ]
