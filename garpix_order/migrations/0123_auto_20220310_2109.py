# Generated by Django 3.0.5 on 2022-03-10 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_order', '0122_auto_20220305_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='cost',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10, verbose_name='Стоимость доставки'),
        ),
        migrations.AlterField(
            model_name='deliverymethod',
            name='type',
            field=models.CharField(choices=[('poland_post', 'Почта Польши'), ('poland_cdek', 'СДЭК Польши'), ('russian_post', 'Почта России'), ('russian_cdek', 'СДЭК России'), ('cargo_with_docs', 'КАРГО (с документами)'), ('cargo_without_docs', 'КАРГО (без доккументов)'), ('cdek', 'СДЭК'), ('post', 'Почта'), ('Five_kg', 'Больше пяти кг.')], max_length=100, unique=True, verbose_name='Тип доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='weight',
            field=models.DecimalField(decimal_places=4, default=0.0, max_digits=10, verbose_name='Вес'),
        ),
    ]
