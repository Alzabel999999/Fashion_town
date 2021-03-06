# Generated by Django 3.0.5 on 2021-01-27 13:05

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_catalog', '0061_auto_20210125_1630'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('garpix_cart_rest', '0006_remove_cartitem_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_active', models.BooleanField(default=True, verbose_name='Включено')),
                ('title', models.CharField(blank=True, default='', max_length=255, verbose_name='Название')),
                ('session', models.CharField(blank=True, default='', max_length=255, verbose_name='Сессия')),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Дополнительные данные')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='WishListItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Цена')),
                ('extra', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, verbose_name='Дополнительные данные')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='garpix_catalog.ProductSku', verbose_name='Продукт')),
                ('wishlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='garpix_cart_rest.WishList', verbose_name='Избранное')),
            ],
            options={
                'verbose_name': 'Товар в избранном',
                'verbose_name_plural': 'Товары в избранном',
            },
        ),
    ]
