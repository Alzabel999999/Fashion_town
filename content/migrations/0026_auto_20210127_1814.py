# Generated by Django 3.0.5 on 2021-01-27 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0025_auto_20210127_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_type',
            field=models.CharField(choices=[('disabled', 'Не показан'), ('main_page_first_page', 'Баннеры на главную (первая страница)'), ('main_page_about', 'Баннер на главную (о компании)'), ('main_page_for_partner', 'Баннеры на главную (для партнёров)')], default='', max_length=100, verbose_name='Тип баннера'),
        ),
    ]
