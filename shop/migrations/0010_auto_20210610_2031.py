# Generated by Django 3.0.5 on 2021-06-10 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20210609_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopconfig',
            name='delivery_method_1_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена доставки 1'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='delivery_method_1_title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Метод доставки 1'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='delivery_method_2_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена доставки 2'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='delivery_method_2_title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Метод доставки 2'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='delivery_method_3_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена доставки 3'),
        ),
        migrations.AddField(
            model_name='shopconfig',
            name='delivery_method_3_title',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Метод доставки 3'),
        ),
    ]