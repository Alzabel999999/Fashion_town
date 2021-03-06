# Generated by Django 3.0.5 on 2021-09-27 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_cart_rest', '0043_auto_20210622_1826'),
        ('user', '0046_user_is_shop_buyer'),
        ('garpix_order', '0102_auto_20210924_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_orders', to='garpix_cart_rest.Cart', verbose_name='Корзина'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_method_orders', to='garpix_order.DeliveryMethod', verbose_name='Метод доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_method_orders', to='garpix_order.PaymentMethod', verbose_name='Метод оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_orders', to='user.Profile', verbose_name='Профиль пользователя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('unformed', 'Заказ не оформлен'), ('payment_waiting', 'Ожидается оплата'), ('in_process', 'Принят в работу'), ('redeemed', 'Заказ выкуплен'), ('packaging', 'Упаковка заказа'), ('delivery_payment_waiting', 'Ожидается оплата за доставку'), ('delivery_paid', 'Доставка оплачена'), ('sended', 'Заказ отправлен'), ('closed', 'Закрыт'), ('canceled', 'Отмена заказа'), ('return', 'Возврат')], default='unformed', max_length=100, verbose_name='Статус заказа'),
        ),
    ]
