# Generated by Django 3.0.5 on 2020-12-21 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0015_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_type',
            field=models.CharField(choices=[('disabled', 'Не показан'), ('main_page_near_slider', 'Баннеры на главную под слайдер'), ('main_page_for_partner', 'Баннеры на главную для партнёров')], default='', max_length=100, verbose_name='Тип баннера'),
        ),
    ]