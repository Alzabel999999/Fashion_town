from django.db import models
from garpix_utils.file_field import get_file_path
from . import Order, Requisites, Delivery, CollectionItem, OrderItem
from user.models import Profile
from django.conf import settings
from django.dispatch import receiver


class Payment(models.Model):
    class STATUS(object):
        EXPECTED = 0
        SUCCESSFULLY = 1
        TYPES = (
            (EXPECTED, 'Ожидается'),
            (SUCCESSFULLY, 'Успешно')
        )

    cost = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2,
                               blank=False, null=False, default=0.00)
    name = models.CharField(max_length=100, verbose_name='Имя отправителя', null=False, blank=False, default='')
    status = models.IntegerField(verbose_name='Статус', default=STATUS.EXPECTED, choices=STATUS.TYPES)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True, default='')
    receipt = models.FileField(verbose_name='Чек', upload_to=get_file_path, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    requisites = models.ForeignKey(Requisites, verbose_name='Реквизиты', on_delete=models.SET_NULL,
                                   blank=False, null=True, related_name='requisite_payments')
    order = models.OneToOneField(Order, verbose_name='Заказ', related_name='order_payment',
                                 null=True, blank=True, on_delete=models.DO_NOTHING)
    delivery = models.OneToOneField(Delivery, verbose_name='Доставка', related_name='delivery_payment',
                                    null=True, blank=True, on_delete=models.DO_NOTHING)
    profile = models.ForeignKey(Profile, verbose_name='Профиль пользователя', related_name='profile_payments',
                                null=True, blank=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'
        ordering = ['-id', ]

    def __str__(self):
        return f'Оплата №{self.id}'

    def set_order_in_process_status(self):
        orders = self.profile.user_orders.filter(status=settings.ORDER_STATUS_PAYMENT_WAITING).order_by('created_at', )
        deliveries = Delivery.objects.filter(status=Delivery.STATUS.DELIVERY_PAYMENT_WAITING,
                                             order__status=settings.ORDER_STATUS_DELIVERY_PAYMENT_WAITING)


        #return orders

        for delivery in deliveries:
            if self.profile.balance >= delivery.cost:
                self.profile.balance -= delivery.cost
                self.profile.save()
                delivery.status = Delivery.STATUS.DELIVERY_PAYMENT_CONFIRMED
                delivery.save()
                self.order.status = settings.ORDER_STATUS_SENDED
                self.order.save()
                from user.models import Notification
                order_url = settings.SITE_URL_FRONT + self.order.order_number
                url = '<a href="{0}">{1}</a>'.format(order_url, self.order.order_number)
                notification = Notification(profile=self.profile, message='С Вашего баланса списано {0}PLN за доставку по заказу № {1}'.format(delivery.cost, url))
                notification.save()
        for order in orders:

            if self.profile.balance >= order.total_cost:
                """try:
                    order_items = order.order_items.all()
                    for order_item in order_items:
                        try:
                            collection_item = CollectionItem.objects.get(order_item=order_item)
                            collection_item.redeemed = True
                            collection_item.save()
                        except:
                            pass

                except:
                    pass"""

                self.profile.balance -= order.total_cost
                self.profile.save()
                order.status = settings.ORDER_STATUS_IN_PROCESS
                order.save()

                order.order_items.all().update(status=settings.ORDER_ITEM_STATUS_PAID)
                from user.models import Notification
                order_url = settings.SITE_URL_FRONT + order.order_number
                url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
                notification = Notification(profile=self.profile, message='С Вашего баланса списано {0}PLN в счет оплаты заказа № {1}'.format(delivery.cost, url))
                notification.save()




        return

    def service(self):
        if self.order:
            return self.order
        if self.delivery:
            return self.delivery
    service.short_description = 'Заказ / доставка'

"""@receiver(models.signals.post_save, sender=Payment)
def change_reddeeme(sender, instance, using, **kwargs):
    #payment = instance
    if instance.status == 1:
        order = instance.order
        #order_items = instance.order.order_items.all()
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            try:
                collection_item = CollectionItem.objects.get(order_item=order_item)
                collection_item.redeemed = True
                collection_item.save()
            except:
                pass"""
