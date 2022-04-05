# Generated by Django 2.1 on 2020-02-04 13:19

from django.db import migrations, models
import garpix_utils.file_field.file_field


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='edition_style',
            field=models.TextField(blank=True, default='', verbose_name='Дополнительные стили'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Изображение'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='is_only_for_authenticated',
            field=models.BooleanField(default=False, verbose_name='Отображать только для вошедших пользователей'),
        ),
    ]
