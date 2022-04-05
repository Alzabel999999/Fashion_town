# Generated by Django 3.0.5 on 2021-06-22 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0020_auto_20210622_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='textprompt',
            name='empty_cart_prompt',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Пустая корзина'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='empty_wishlist_prompt',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Пустое избранное'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='information_sizes_prompt',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Информация - Размеры'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='lk_export_photo_prompt',
            field=models.TextField(blank=True, default='Выделите нужные фото и нажмите на кнопку “Скачать выбранные”, чтобы скачать фото одним архивом. Для дропшипперов действует ограничение на скачивание: не более 50 штук в день, если нет созданного интернет-магазина на платформе Fashion Town. Для оптовых покупателей нет ограничений на скачивание.', null=True, verbose_name='Личный кабинет - Скачать фото'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='lk_notifications_prompt',
            field=models.TextField(blank=True, default='В этом разделе отображаются все уведомления о событиях на платформе. Вы можете выбрать ненужные уведомлений и удалить их. Чтобы прочесть полный текст уведомления, нажмите на него.', null=True, verbose_name='Личный кабинет - Уведомления'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='main_catalog_prompt',
            field=models.TextField(blank=True, default='Здесь представлены все товары платформы, в том числе те, которые продаются под заказ. Если вы хотите посмотреть только товары в наличии, воспользуйтесь фильтром “В наличии”.', null=True, verbose_name='Главная страница - Каталог'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='main_in_stock_prompt',
            field=models.TextField(blank=True, default='Здесь отображаются товары, которые есть в наличии. Внимание! Количество товара ограничено. Товар резервируется за покупателем после поступления оплаты. Товар в корзине не считается купленным.', null=True, verbose_name='Главная страница - Товары в наличии'),
        ),
        migrations.AddField(
            model_name='textprompt',
            name='order_wait_call_prompt',
            field=models.TextField(blank=True, default='', null=True, verbose_name='Заказ - Дождаться звонка'),
        ),
    ]
