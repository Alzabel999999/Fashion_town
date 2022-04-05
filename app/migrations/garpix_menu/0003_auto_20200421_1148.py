# Generated by Django 2.1 on 2020-04-21 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_menu', '0002_auto_20200204_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='menu_type',
            field=models.CharField(choices=[('disabled', 'Not shown'), ('main_menu', 'Main menu'), ('header_menu', 'Header menu'), ('footer_menu', 'Footer menu')], default='', max_length=100, verbose_name='Тип меню'),
        ),
    ]
