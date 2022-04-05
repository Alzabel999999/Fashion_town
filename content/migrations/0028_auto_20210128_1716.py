# Generated by Django 3.0.5 on 2021-01-28 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0061_auto_20210125_1630'),
        ('content', '0027_review_reviewphoto_reviewvideo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Обзор', 'verbose_name_plural': 'Обзоры'},
        ),
        migrations.AlterModelOptions(
            name='reviewphoto',
            options={'verbose_name': 'Фото', 'verbose_name_plural': 'Фото'},
        ),
        migrations.AlterModelOptions(
            name='reviewvideo',
            options={'verbose_name': 'Видео', 'verbose_name_plural': 'Видео'},
        ),
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_review', to='garpix_catalog.ProductSku', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='review',
            name='stars',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5, verbose_name='Кол-во звезд'),
        ),
    ]
