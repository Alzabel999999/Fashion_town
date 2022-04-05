# Generated by Django 3.0.5 on 2021-06-11 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0079_auto_20210610_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='page_type',
            field=models.IntegerField(choices=[(0, 'default'), (1, 'Главная'), (5, 'Каталог'), (3, 'Категория'), (4, 'Товар'), (2, 'Информация'), (6, 'Авторизация'), (7, 'Регистрация'), (8, 'ЛК'), (9, 'Корзина'), (10, 'Вспомнить пароль'), (11, 'Оформление заказа'), (12, 'История заказов'), (13, 'Избранное'), (14, 'Сравнение'), (15, 'Поиск'), (16, 'Информация (оплата)'), (17, 'Информация (доставка)'), (18, 'Информация (замена)'), (19, 'Информация (юридическая информация)'), (20, 'Информация (контакты)'), (21, 'Информация (как подобрать размер)'), (22, 'Информация (отзывы)'), (23, 'О нас'), (24, 'Живые фото'), (25, 'Живые фото (детальная)'), (26, 'Новости'), (27, 'Новости (детальная)'), (28, 'Партнерам'), (29, 'Заказы'), (30, 'Заказ (детальная)'), (31, 'Отзывы (ЛК)'), (32, '404'), (33, '500'), (34, 'Профиль'), (35, 'Уведомления'), (36, 'Баланс и платежи'), (37, 'Экспорт каталога'), (38, 'Мой магазин'), (39, 'Мой магазин (настройки)'), (40, 'Мой магазин (реквизиты)'), (41, 'Мой магазин (контент)'), (42, 'Мой магазин (контент - информация для розницы)'), (43, 'Мой магазин (контент - о компании)'), (44, 'Мой магазин (контент - контакты)'), (45, 'Мой магазин (контент - живые фото)'), (46, 'Мой магазин (контент - футер сайта)'), (47, 'Мой магазин (контент - доставка)'), (48, 'Мой магазин (создание)'), (49, 'Мой магазин (товары)'), (50, 'Мой магазин (заказы)'), (51, 'Мой магазин (заказ - детальная страница)'), (52, 'Мой магазин (клиенты)'), (53, 'Мой магазин (промокоды)'), (54, 'Мой магазин (клиент - детальная страница)'), (55, 'Лендинг'), (56, 'UIKit'), (57, 'Главная (ИМ)'), (58, 'Информация (ИМ)'), (59, 'Каталог (ИМ)'), (60, 'Товар (ИМ)'), (61, 'Оформление заказа (ИМ)'), (62, 'Заказы (ИМ)'), (63, 'Заказ - детальная (ИМ)'), (64, 'Живые фото - детальная (ИМ)'), (65, 'Живые фото (ИМ)'), (66, 'Корзина (ИМ)'), (67, 'Мой магазин (Описание)'), (68, 'Мой магазин (Информация)'), (69, 'Мой магазин (Мотивационный блок)'), (70, 'Мой магазин (контент - главная)')], default=27, verbose_name='Тип страницы'),
        ),
    ]
