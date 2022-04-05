from decimal import Decimal
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from garpix_catalog.models import ProductSku
from ..models.order import Order
from django.dispatch import receiver
from ..models.order_item_comment_photo import OrderItemCommentPhoto

from garpix_cart_rest.models import CartItem, CartItemsPack
import garpix_utils.file_field.file_field
import logging


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE, related_name='order_items',blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, verbose_name='Название', default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Новая цена', blank=True, null=True)
    product = models.ForeignKey(ProductSku, blank=True, null=True, verbose_name='Товар', on_delete=models.SET_NULL,
                                related_name='product_ordered_skus')
    extra = JSONField(blank=True, verbose_name='Дополнительные данные', default=dict)
    fixed_price = models.DecimalField(verbose_name='Фиксированная цена', decimal_places=2,
                                      max_digits=10, default=0.00)
    status = models.CharField(default=settings.ORDER_ITEM_STATUS_PAYMENT_WAITING, max_length=20,
                              choices=settings.CHOICE_ORDER_ITEM_STATUSES, verbose_name='Статус')
    total_price = models.DecimalField(verbose_name='Цена', decimal_places=2, blank=True, null=True,
                                      max_digits=10, default=0.00)
    cart_item = models.ForeignKey(CartItem, verbose_name='Товар в корзине', related_name='cart_item_order_items',
                                  on_delete=models.SET_NULL, blank=True, null=True)
    cart_items_pack = models.ForeignKey(
        CartItemsPack, verbose_name='Пачка товаров в корзине', related_name='cart_items_pack_order_items',
        on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True, null=True, default='')
    #file = models.ImageField(blank=True, null=True, upload_to=garpix_utils.file_field.file_field.get_file_path, verbose_name='Файл комментария')
    change_agreement = models.BooleanField(verbose_name='Согласие на замену', default=True)

    class Meta:
        verbose_name = 'Товар заказа'
        verbose_name_plural = 'Товары заказа'

    def __str__(self):
        return f'{self.id} - {self.product.__str__()}'

    def profile(self):
        try:
            return self.order.profile
        except:
            return '-'
    profile.short_description = 'Профиль пользователя'

    def get_additional_purchase(self):
        # todo переделать под новый get_condition
        # if self.order.status == settings.ORDER_ITEM_STATUS_ORDERED:
        #     condition = self.product.get_condition()
        #     if condition is None or condition.order_type == 0:
        #         return None
        #     product = self.product
        #     color = product.color
        #     product_base = product.product
        #     products = None
        #     # размерный ряд
        #     if condition.order_type == 1:
        #         print('***---*** # размерный ряд')
        #         products = ProductSku.objects.filter(product=product_base, color=color)
        #         if condition.number in (0, 1):
        #             products = products.exclude(id=product.id)
        #     # упаковка
        #     if condition.order_type == 2:
        #         print('***---*** # упаковка')
        #         products = ProductSku.objects.filter(id=self.product.id)
        #     # минимум
        #     if condition.order_type == 3:
        #         print('***---*** # минимум')
        #         products = ProductSku.objects.filter(product__brand=product_base.brand)
        #         if condition.is_min_for_model:
        #             products = products.filter(product=product_base)
        #     return products
        return None

    def freezing_price(self):
        self.fixed_price = self.product.product.price
        self.save()

    def get_prices(self):
        if not self.price:
            if self.cart_item:
                if self.cart_item.price == self.cart_item.total_item_price:
                    return 0.00, self.cart_item.total_item_price
                else:
                    return self.cart_item.total_item_price, self.cart_item.price
            if self.cart_items_pack:
                if not self.cart_items_pack.old_price or self.cart_items_pack.old_price == Decimal('0.00'):
                    return 0.00, self.cart_items_pack.price
                else:
                    return self.cart_items_pack.price, self.cart_items_pack.old_price
        return self.price, self.fixed_price

    def get_total_price(self):
        if self.price:
            return self.price
        else:
            return self.fixed_price

    def save(self, *args, **kwargs):
        from ..models import Collection
        self.price, self.fixed_price = self.get_prices()
        super(OrderItem, self).save()
        self.total_price = self.get_total_price()
        super(OrderItem, self).save()
        profile = self.order.profile
        from user.models import Notification
        order_url = settings.SITE_URL_FRONT + self.order.order_number
        url = '<a href="{0}">{1}</a>'.format(order_url, self.order.order_number)
        if self.status != 'collection':
            notification = Notification(profile=profile, message='Статус Вашего товара заказа № {0} изменен на {1} '.format(url, settings.ORDER_ITEM_STATUSES[self.status]['title']))
            notification.save()
        #order_items = self.order.order_items.all()
        #if self.status == settings.ORDER_ITEM_STATUS_REDEEMED:

            #status = False
            #if self.product.product.product_rc.rc_type == 1:
                #from ..models.collection_item import CollectionItem
                #collection_item = CollectionItem.objects.get(order_item=self)
                #collection_item.paid = True
                #collection_item.save()
            #if len(order_items.exclude(status='redeemed')) == 0 and len(order_items.include(status=''))!=0:
                #self.order.status = 'redeemed'
                #self.order.save()
        #if self.status == settings.ORDER_ITEM_STATUS_CANCELED:
            #if len(order_items) == 0:
                #self






        """if self.status == settings.ORDER_ITEM_STATUS_PAID:
            if self.product.product.get_condition().rc_type in [1, 2]:
                Collection.add_to_some_collection(self)
            sku = ProductSku.objects.filter(id=self.product.id).first()
            if sku.product.is_in_stock:
                if sku.in_stock_count > 0:
                    sku.in_stock_count -= 1
                    sku.save()
                else:
                    self.status = settings.ORDER_ITEM_STATUS_REPLACEMENT
                    super(OrderItem, self).save(*args, **kwargs)"""

    def brand(self):
        if self.cart_item:
            return self.cart_item.product.product.brand
        elif self.cart_items_pack:
            return self.cart_items_pack.product.brand
        else:
            return ''

    def size(self):
        return self.product.size

    def color(self):
        return self.product.color

    def purchase_title(self):
        return self.product.product.title if self.product else f'product_{self.id}'

    def purchase_size(self):
        return self.product.size if self.product else f'size_of_product_{self.id}'

    def purchase_color(self):
        return self.product.color if self.product else f'color_of_product_{self.id}'

    def purchase_brand(self):
        if self.cart_item:
            return self.cart_item.product.product.brand
        elif self.cart_items_pack:
            return self.cart_items_pack.product.brand
        else:
            return ''

    def purchase_order(self):
        try:
            return self.order.order_number
        except:
            return '-'

    def get_same_order_items(self):
        order = self.order
        same_order_items = order.order_items.filter(
            product=self.product, cart_item=self.cart_item, cart_items_pack=self.cart_items_pack)
        return same_order_items



    def update_item(self, request):
        if 'change_agreement' in request.POST.keys():
            self.change_agreement = request.POST.get('change_agreement')
        if 'comment' in request.POST.keys():
            self.comment = request.POST.get('comment')
        if request.FILES:
            self.order_item_comment_photos.all().delete()
            for file in request.FILES.getlist('files'):
                if 'image' in file.content_type and file.size < 3000000:
                    OrderItemCommentPhoto.objects.create(order_item=self, image=file)
        self.save()
        return None

@receiver(models.signals.post_save, sender=OrderItem)
def check_collection_post(sender, instance, using, **kwargs):
    #if instance.product.product.product_rc:
        #if instance.product.product.product_rc.rc_type == 1:
    if instance.status == 'canceled' or instance.status == 8 or instance.status == 'Отмена товара':
        from ..models.collection_item import CollectionItem
        try:
            collection_item = CollectionItem.objects.get(order_item=instance)
            collection_item.order_item = None
            collection_item.save()
        except:
            pass
    if instance.status == 'paid' or instance.status == 2 or instance.status == 'Товар оплачен':
        from ..models.collection_item import CollectionItem
        try:
            collection_item = CollectionItem.objects.get(order_item=instance)
            if collection_item.collection.status != 1:
                if collection_item.redeemed == False:
                    collection_item.redeemed = True
                    collection_item.save()
        except:
            pass
    if instance.status == 'redeemed':
        order_items = instance.order.order_items.all()
        order_items_redeemed = instance.order.order_items.all().filter(status='reddemed')
        if len(order_items) == len(order_items_redeemed):
            instance.order.status = 'redeemed'
            instance.order.save()

@receiver(models.signals.pre_delete, sender=OrderItem)
def check_collection(sender, instance, using, **kwargs):
    try:
        if instance.product.product.product_rc:
            if instance.product.product.product_rc.rc_type == 1:
                from ..models.collection_item import CollectionItem
                try:
                    collection_item = CollectionItem.objects.get(order_item=instance)
                    collection_item.order_item = None
                    collection_item.redeemed = False
                    collection_item.save()
                except:
                    pass
    except:
        pass
