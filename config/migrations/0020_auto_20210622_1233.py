# Generated by Django 3.0.5 on 2021-06-22 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0019_auto_20210622_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textprompt',
            name='shop_settings_main_catalog_prompt',
            field=models.TextField(blank=True, default='Выберите те товары, которые Вы хотите отобразить на Вашем сайте, и нажмите на кнопку “В свой каталог”. По умолчанию товар копируется с ценой, указанной в поле “Цена для вас”. Если Вы указываете наценку на категории, то к “Цене для вас” прибавляется эта наценка. Если Вы указываете персональную цену в поле “Ваша цена”, то товар отображается с ней, наценка на категорию не учитывается.', null=True, verbose_name='Настройки ИМ - Основной каталог'),
        ),
        migrations.AlterField(
            model_name='textprompt',
            name='shop_settings_my_catalog_prompt',
            field=models.TextField(blank=True, default='Для удаления товаров из Вашего каталога необходимо выделить их галочкой. Появится кнопка “Удалить”, после нажатия на которую товары выбранные товары будут удалены из Вашего интернет-магазина. На этой же странице Вы можете редактировать цены на товары и наценки на категории. По умолчанию товар копируется с ценой, указанной в поле “Цена для вас”. Если Вы указываете наценку на категории, то к “Цене для вас” прибавляется эта наценка. Если Вы указываете персональную цену в поле “Ваша цена”, то товар отображается с ней, наценка на категорию не учитывается.', null=True, verbose_name='Настройки ИМ - Мой каталог'),
        ),
    ]
