# Generated by Django 3.0.5 on 2021-05-14 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0114_auto_20210513_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_one_size',
            field=models.BooleanField(default=False, verbose_name='Товар без размера'),
        ),
    ]
