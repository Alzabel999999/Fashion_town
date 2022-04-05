from decimal import Decimal
from django.contrib.sites.models import Site
from django.db.models import F, Sum
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from garpix_page.models import Page
from garpix_order.models.payment_method import PaymentMethod
#from garpix_order.models.payment import Payment
from garpix_utils.file_field import get_file_path
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from datetime import datetime
from ..mixin import PassportMixin
from .service import Service
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.db import transaction
from user.models import Notification
#from .signals import delete_question


class Order(AbstractBasePageModel, PassportMixin):
    title = None
    page_type = models.IntegerField(
        default=settings.PAGE_TYPE_ORDER_DETAIL, verbose_name='Тип страницы', choices=settings.CHOICES_PAGE_TYPES)

    profile = models.ForeignKey('user.Profile', verbose_name='Профиль пользователя', related_name='user_orders',
                                on_delete=models.SET_NULL, blank=True, null=True)
    cart = models.ForeignKey('garpix_cart_rest.Cart', verbose_name='Корзина', related_name='cart_orders',
                             on_delete=models.SET_NULL, blank=True, null=True)
    delivery_method = models.ForeignKey('DeliveryMethod', verbose_name='Метод доставки',
                                        related_name='delivery_method_orders',
                                        on_delete=models.SET_NULL, blank=True, null=True)
    delivery_address = models.ForeignKey('DeliveryAddress', verbose_name='Адрес доставки',
                                         related_name='delivery_address_orders',
                                         on_delete=models.SET_NULL, blank=True, null=True)
    payment_method = models.ForeignKey('PaymentMethod', verbose_name='Метод оплаты',
                                       related_name='payment_method_orders',
                                       on_delete=models.CASCADE, blank=True, null=True)#CASCADE
    status = models.CharField(default=settings.ORDER_STATUS_UNFORMED, max_length=100,
                              choices=settings.CHOICE_ORDER_STATUSES, verbose_name='Статус заказа')
    old_status = models.CharField(default=settings.ORDER_STATUS_UNFORMED, max_length=100,
                              choices=settings.CHOICE_ORDER_STATUSES, verbose_name='Старый статус заказа')
    extra = JSONField(blank=True, verbose_name='Дополнительные данные', default=dict)

    weight = models.DecimalField(verbose_name='Вес', decimal_places=4,
                                 max_digits=10, default=0.00)
    order_cost = models.DecimalField(verbose_name='Стоимость заказа', decimal_places=2,
                                     max_digits=10, default=0.00)
    discount = models.DecimalField(verbose_name='Скидка', decimal_places=2,
                                   max_digits=10, default=0.00)
    delivery_cost = models.DecimalField(verbose_name='Цена доставки', decimal_places=2,
                                        max_digits=10, default=0.00)
    total_cost = models.DecimalField(verbose_name='Итоговая цена', decimal_places=2,
                                     max_digits=10, default=0.00)

    order_number = models.CharField(max_length=100, verbose_name='Номер заказа', blank=True, null=True, default='')
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True)

    sites = models.ManyToManyField(
        Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    parent = models.ForeignKey(Page, null=True, blank=True, db_index=True, verbose_name='Родительская страница',
                               on_delete=models.SET_NULL, limit_choices_to={'page_type': settings.PAGE_TYPE_ORDERS})

    track_number = models.CharField(max_length=100, verbose_name='Трек номер', blank=True, null=True, default='')
    specification = models.FileField(verbose_name='Спецификация', upload_to=get_file_path,
                                     blank=True, null=True, default=None)

    services = models.ManyToManyField(Service, verbose_name='Доп. услуги', related_name='service_orders', blank=True)
    total_services_cost = models.DecimalField(verbose_name='Цена доп. услуг', decimal_places=2, null=True,
                                              max_digits=10, default=0.00)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-id',)

    def __str__(self):
        return f'Order №{self.id}'

    # @property
    def get_order_total(self):
        return self.order_items.aggregate(
            total=Sum(F('total_price'), output_field=models.DecimalField(decimal_places=2, max_digits=10)))['total']

    # def change_status(self):
    #     order_items = self.order_items.all()
    #     for item in order_items:
    #         if item.qty <= item.product.in_stock_count and item.status == self.ORDER_STATUS_IN_PROCESS:
    #             item.status = settings.ORDER_ITEM_STATUS_REDEEMED
    #     self.save()

    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)
        if not self.order_number:
            self.order_number = self.create_order_number()
            super(Order, self).save()
        if not self.slug:
            self.slug = self.order_number
        if not self.title:
            self.title = self.order_number
        self.order_cost = self.order_items.all().aggregate(order_cost=Sum('total_price'))['order_cost']
        self.delivery_cost = self.order_delivery.cost if hasattr(self, 'order_delivery') else Decimal('0.00')
        self.total_services_cost = self.services.all().aggregate(cost_sum=Sum('cost'))['cost_sum']
        if not self.order_cost:
            self.order_cost = Decimal('0.00')
        if not self.delivery_cost:
            self.delivery_cost = Decimal('0.00')
        if not self.total_services_cost:
            self.total_services_cost = Decimal('0.00')
        super(Order, self).save(*args, **kwargs)
        self.total_cost = self.order_cost + self.delivery_cost + self.total_services_cost
        super(Order, self).save(*args, **kwargs)
        if self.status == settings.ORDER_STATUS_PACKAGING:
            order_items = self.order_items.all()
            for order_item in order_items:
                order_item.status = 'packaging'
                order_item.save()
        if self.status == settings.ORDER_STATUS_SENDED:
            order_items = self.order_items.all()
            for order_item in order_items:
                order_item.status = 'sended'
                order_item.save()






    def create_order_number(self):
        return f"{datetime.strftime(self.created_at, '%Y%m%d%H%M')}-{str(self.id)}"

    def get_brands(self):
        order_items = self.order_items.filter(status__in=[settings.ORDER_ITEM_STATUS_REDEEMED, settings.ORDER_ITEM_STATUS_ORDERED])#, settings.ORDER_ITEM_STATUS_PAID, settings.ORDER_ITEM_STATUS_PAYMENT_WAITING
        brands = []
        for item in order_items:
            if item.cart_item:
                brand = item.cart_item.product.product.brand
            elif item.cart_items_pack:
                brand = item.cart_items_pack.product.brand
            else:
                brand = None
            if brand not in brands:
                brands.append(brand)
        return brands

    def items_count(self):
        return self.order_items.all().count()

    @classmethod
    def get_unformed_order(cls, profile):
        unformed_orders = profile.user_orders.filter(status=settings.ORDER_STATUS_UNFORMED)
        if unformed_orders.count() > 1:
            last_unformed_order = unformed_orders.first()
            unformed_orders.exclude(id=last_unformed_order.id).delete()
            return last_unformed_order
        elif unformed_orders.count() == 1:
            return unformed_orders.first()
        else:
            order = cls(profile=profile, cart=profile.cart)
            order.save()
            return order


@receiver(models.signals.pre_delete, sender=Order)
def delete_question(sender, instance, using, **kwargs):
    from .payment import Payment
    try:
        payment = Payment.objects.get(order=instance)
        payment.order = None
        payment.save()
        #payment.delete()
    except:
        pass



"""@receiver(models.signals.post_save, sender=Order)
def change_order(sender, instance, using, **kwargs):
    order = instance
    profile = instance.profile
    notification = Notification(profile=profile, message='status ' +  instance.status)
    notification.save()
    notification = Notification(profile=profile, message='oldstatus ' + instance.old_status)
    notification.save()
    if instance.status != instance.old_status:

        order_url = settings.SITE_URL_FRONT + order.order_number
        url = '<a href="{0}">{1}</a>'.format(order_url, order.order_number)
        notification = Notification(profile=profile, message='Статус Вашего заказа № {0} изменен на {1} '.format(url, settings.ORDER_STATUSES[order.status]['title']))
        notification.save()"""
