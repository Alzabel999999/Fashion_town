from django.db import models
from . import Order
from user.models import Notification


class Delivery(models.Model):

    class STATUS:
        DELIVERY_PAYMENT_WAITING = 'delivery_payment_waiting'
        DELIVERY_PAYMENT_CONFIRMED = 'delivery_payment_confirmed'
        TYPES = (
            (DELIVERY_PAYMENT_WAITING, 'Ожидается оплата'),
            (DELIVERY_PAYMENT_CONFIRMED, 'Оплачено'),
        )

    order = models.OneToOneField(Order, verbose_name='Заказ', related_name='order_delivery', on_delete=models.CASCADE)
    cost = models.DecimalField(verbose_name='Стоимость доставки', max_digits=10, decimal_places=4, default=0.00)
    status = models.CharField(
        max_length=40, verbose_name='Статус', choices=STATUS.TYPES, default=STATUS.DELIVERY_PAYMENT_WAITING)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ('-id',)

    def __str__(self):
        return f'Доставка заказа №{self.order.id}'

    def profile(self):
        return self.order.profile

    """def save(self, *args, **kwargs):
        if self.cost != 0:
            profile = self.order.profile
            notification = Notification(profile=profile, message='Вам нужно оплатить доставку товара {0} на сумму {1}'.format(self.order.id, self.cost))
            notification.save()"""

    profile.short_description = 'Профиль пользователя'
