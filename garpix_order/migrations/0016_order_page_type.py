# Generated by Django 3.0.5 on 2021-02-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0015_auto_20210211_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='page_type',
            field=models.IntegerField(choices=[(0, 'default'), (1, 'Главная'), (5, 'Каталог'), (3, 'Категория'), (4, 'Продукт'), (2, 'Информация'), (6, 'Авторизация'), (7, 'Регистрация'), (8, 'ЛК'), (9, 'Корзина'), (10, 'Вспомнить пароль'), (11, 'Оформление заказа'), (12, 'История заказов'), (13, 'Избранное'), (14, 'Сравнение'), (15, 'Поиск'), (16, 'Информация (оплата)'), (17, 'Информация (доставка)'), (18, 'Информация (замена)'), (19, 'Информация (юридическая информация)'), (20, 'Информация (контакты)'), (21, 'Информация (как подобрать размер)'), (22, 'Информация (отзывы)'), (23, 'О нас'), (24, 'Живые фото'), (25, 'Живые фото (детальная)'), (26, 'Новости'), (27, 'Новости (детальная)'), (28, 'Партнерам'), (29, 'Заказы'), (30, 'Заказ (детальная)')], default=30, verbose_name='Тип страницы'),
        ),
    ]
