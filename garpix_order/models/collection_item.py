from django.db import models
from ..models.collection import Collection
from ..models.order_item import OrderItem
from garpix_catalog.models import ProductSku
from django.dispatch import receiver
import time
from django.conf import settings


class CollectionItem(models.Model):

    collection = models.ForeignKey(Collection, verbose_name='Сбор', related_name='collection_items',
                                   blank=False, null=False, on_delete=models.CASCADE)
    sku = models.ForeignKey(ProductSku, verbose_name='Товар', related_name='sku_collection_items',
                            blank=True, null=True, default=None, on_delete=models.SET_NULL)
    redeemed = models.BooleanField(verbose_name='Оплачено', default=False)
    paid = models.BooleanField(verbose_name='Выкуплено', default=False)
    order_item = models.OneToOneField(OrderItem, verbose_name='Позиция в заказе',
                                      related_name='order_item_collection_item',
                                      blank=True, null=True, default=None, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Товар в сборе'
        verbose_name_plural = 'Товары в сборе'
        ordering = ['-redeemed', '-id', ]

    def __str__(self):
        return f'{self.collection} - {self.sku}'


@receiver(models.signals.post_save, sender=CollectionItem)
def check_condition(sender, instance, using, **kwargs):
    #time.sleep(1)
    collection = instance.collection
    status = True
    #collection_items = CollectionItem.objects.filter(collection=collection)
    collection_items_all = CollectionItem.objects.filter(collection=collection)
    collection_items = collection.collection_items.all().exclude(redeemed=True)
    collection_sizes = collection.product.product_rc.sizes.all()
    if instance.paid == True or instance.paid == 'True' or instance.paid == 'true':
        instance.order_item.status = 'redeemed'
        instance.order_item.save()
    if len(collection_items)> 0 and len(collection_sizes) == len(collection_items_all):
        status = False
    if len(collection_items_all) != len(collection_sizes):
        status = False
    if status == True:#and len(collection_items_all)==0:
        collection.status = 1
        collection.save()
        #time.sleep(8)
        from user.models import Notification
        for collection_item in collection.collection_items.all():
            profile = collection_item.order_item.order.profile
            product_url = settings.SITE_URL_FRONT + collection_item.order_item.product.product.get_slug()
            order_url = settings.SITE_URL_FRONT + collection_item.order_item.order.order_number
            url1 = '<a href="{0}">{1}</a>'.format(order_url, collection_item.order_item.order.order_number)
            url2 = '<a href="{0}">{1}</a>'.format(product_url, collection_item.order_item.product.title)
            notification = Notification(profile=profile, message='Товар {0} в заказе № {1} принят к выкупу! '.format(url2, url1))
            notification.save()
            #collection_item.order_item.status = 'paid'
            #collection_item.order_item.save()
        #collection_items_1 = collection.collection_items.all()
        #for collection_item_1 in collection_items_1:
            #collection_item_1.order_item.status = 'paid'
            #collection_item_1.order_item.save()
        #for collection_item in collection_items_all:
            #collection_item.order_item.status = 'paid'
            #collection_item.order_item.save()
    if status == False:
        collection.status = 0
        collection.save()
    """if len(collection_items) == 0 and collection.status == 1:
        for collection_item in collection_items:
            collection_item.order_item = None
            collection_item.save()
        collection.delete()"""
