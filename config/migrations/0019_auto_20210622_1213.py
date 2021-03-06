# Generated by Django 3.0.5 on 2021-06-22 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0018_textprompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_about_prompt',
            field=models.TextField(blank=True, default='Фотография и краткий текст о компании будут отображаться на главной странице Вашего интернет-магазина в блоке “О компании”. Полный текст о компании - на странице “О компании”. Для сохранения и публикации изменений нажмите на кнопку “Применить”.', null=True, verbose_name='Настройки ИМ - Контент - О компании'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_contacts_prompt',
            field=models.TextField(blank=True, default='Заполните поля в форме ниже, чтобы они отобразились на странице “Контакты” Вашего сайта. Незаполненные поля не будут выводиться. В поле “Краткий текст” Вы можете указать дополнительные контактные данные.', null=True, verbose_name='Настройки ИМ - Контент - Контакты'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_delivery_prompt',
            field=models.TextField(blank=True, default='Здесь Вам необходимо указать способы доставки, которые будут выводиться Вашим покупателям при оформлении заказа. Укажите короткое название способа доставки и его стоимость. Можно указать не более трех способов. Для сохранения изменения нажмите на кнопку “Применить”.', null=True, verbose_name='Настройки ИМ - Контент - Доставка'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_footer_prompt',
            field=models.TextField(blank=True, default='Заполните поля в форме ниже, чтобы они отобразились в футере на всех страницах Вашего сайта. Чтобы логотип был на прозрачном фоне, его необходимо загружать в формате png. Для отображения иконок соц. сетей укажите ссылки на Ваши страницы.', null=True, verbose_name='Настройки ИМ - Контент - Футер'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_information_prompt',
            field=models.TextField(blank=True, default='Текст, добавленный в этом разделе, будет отображаться на странице “Информация” Вашего интернет-магазина. Переключайтесь по вкладкам выше, чтобы добавить текст во все блоки страницы. Для сохранения и публикации изменений нажмите на кнопку “Применить”.', null=True, verbose_name='Настройки ИМ - Контент - Информация'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_live_photos_prompt',
            field=models.TextField(blank=True, default='Для копирования фотографий в Ваш интернет-магазин Вам необходимо проставить галочки чекбоксы у нужных альбомов и нажать на кнопку “Применить”. Чтобы удалить фотографии со своего сайта, необходимо снять галочки у фото и нажать на кнопку “Применить”. Название альбомов можно редактировать.', null=True, verbose_name='Настройки ИМ - Контент - Живые фото'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_content_main_prompt',
            field=models.TextField(blank=True, default='В этом разделе Вы можете заполнить контент, который будет отображаться на главной странице Вашего интернет-магазина. Загрузите баннер для первого экрана и баннеры для блоков “Новинки”, “Хиты сезона”, “Распродажа”. Для сохранения и публикации изменений нажмите на кнопку “Применить”.', null=True, verbose_name='Настройки ИМ - Контент - Главная'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_main_catalog_prompt',
            field=models.TextField(blank=True, default='Выберите те товары, которые вы хотите добавить на свой сайт. Затем нажмите кнопку “Добавить в свой каталог” для экспорта товаров. Также Вы можете сохранить любой товар в избранное (при этом товар не будет добавлен в Ваш каталог).', null=True, verbose_name='Настройки ИМ - Основной каталог'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='shop_settings_my_catalog_prompt',
            field=models.TextField(blank=True, default='Для удаления товаров из Вашего каталога необходимо выделить их галочкой. Появится кнопка “Удалить”, после нажатия на которую товары выбранные товары будут удалены из Вашего интернет-магазина. На этой же странице Вы можете редактировать цены на товары и наценки на категории.', null=True, verbose_name='Настройки ИМ - Мой каталог'),
        ),
    ]
