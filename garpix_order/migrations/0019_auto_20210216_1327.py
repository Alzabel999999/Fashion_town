# Generated by Django 3.0.5 on 2021-02-16 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('garpix_cart_rest', '0009_auto_20210216_1327'),
        ('garpix_order', '0018_auto_20210211_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correspondence',
            name='order',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_correspondence', to='garpix_order.Order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='correspondenceitem',
            name='correspondence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='correspondence_items', to='garpix_order.Correspondence', verbose_name='Переписка'),
        ),
        migrations.AlterField(
            model_name='correspondenceitem',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_correspondence_items', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_addresses', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart_orders', to='garpix_cart_rest.Cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_address_orders', to='garpix_order.DeliveryAddress', verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_method_orders', to='garpix_order.DeliveryMethod', verbose_name='Метод доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_method_orders', to='garpix_order.PaymentMethod', verbose_name='Метод оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='requisites',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisite_orders', to='garpix_order.Requisites', verbose_name='Реквизиты по заказу'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='requisites',
            name='requisites',
            field=models.TextField(blank=True, default='', verbose_name='Реквизиты'),
        ),
    ]
