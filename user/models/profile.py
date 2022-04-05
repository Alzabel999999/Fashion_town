from django.db import models
from .user import User
from garpix_catalog.models import Product

from django.conf import settings


class ProfileManager(models.Manager):

    def get_queryset(self):
        return super(ProfileManager, self).get_queryset().annotate(rating=models.Sum('profile_reviews__likes_count'))


class Profile(models.Model):

    class ROLE:
        UNREGISTRED = 0
        RETAIL = 1
        DROPSHIPPER = 2
        WHOLESALE = 3
        TYPES = (
            (UNREGISTRED, 'Незарегистрированный пользователь'),
            (RETAIL, 'Розничный покупатель'),
            (DROPSHIPPER, 'Дропшиппер'),
            (WHOLESALE, 'Оптовый покупатель'),
        )

    class INFO_SOURCE:
        INTERNET_RECLAIM = 1
        SOCIAL_NETWORK = 2
        ACQUAINTANCES = 3
        OTHER = 4
        TYPES = (
            (INTERNET_RECLAIM, 'Реклама в интернете'),
            (SOCIAL_NETWORK, 'Из социальных сетей'),
            (ACQUAINTANCES, 'От знакомых'),
            (OTHER, 'Другое'),
        )

    user = models.OneToOneField(User, verbose_name='Пользователь', related_name='profile', on_delete=models.CASCADE)
    role = models.IntegerField(verbose_name='Роль пользователя', default=ROLE.UNREGISTRED, choices=ROLE.TYPES)

    vk_link = models.CharField(verbose_name='Ссылка на VK', max_length=512, blank=True, null=True, default='')
    insta_link = models.CharField(verbose_name='Ссылка на Instagram', max_length=512, blank=True, null=True, default='')
    other_link = models.CharField(verbose_name='Ссылка на другую соцсеть', max_length=512, blank=True, null=True, default='')
    site_link = models.CharField(verbose_name='Ссылка на сайт', max_length=512, blank=True, null=True, default='')

    inn = models.CharField(verbose_name='ИНН', max_length=512, blank=True, null=True, default='')
    organization = models.CharField(verbose_name='Организации', max_length=512, blank=True, null=True, default='')

    passport_number = models.CharField(max_length=16, verbose_name='Номер',
                                       blank=True, null=True, default='')
    passport_issued = models.CharField(max_length=255, verbose_name='Кем выдан', blank=True, null=True, default='')
    passport_issue_date = models.DateField(verbose_name='Дата выдачи', blank=True, null=True, default=None)

    from_where_known = models.IntegerField(
        verbose_name='Откуда узнали', default=INFO_SOURCE.OTHER, choices=INFO_SOURCE.TYPES)
    shop_link = models.CharField(verbose_name='Ссылка на магазин', max_length=512, blank=True, null=True, default='')

    balance = models.DecimalField(verbose_name='Баланс', default=0.00, max_digits=10, decimal_places=2)
    receive_newsletter = models.BooleanField(verbose_name='Получать рассылку', default=True)

    objects = ProfileManager()

    download_count = models.PositiveIntegerField(verbose_name='Скачано фотографий, шт', default=0)

    def passive_balance(self):
        pb = self.profile_payments.filter(status=0).aggregate(passive_balance=models.Sum('cost'))['passive_balance']
        return pb
    passive_balance.short_description = 'Пассивный баланс'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'Профиль пользователя {self.user}'

    def save(self, *args, **kwargs):
        if self.id:
            old_balance = Profile.objects.get(id=self.id).balance
            super(Profile, self).save(*args, **kwargs)
            if old_balance != self.balance:
                if old_balance < self.balance:
                    if self.role in [2, 3]:
                        if self.role == 2:
                            if self.get_unpaid_deliveries():
                                self.balance = self.pay_delivery()
                                super(Profile, self).save(*args, **kwargs)
                        if self.get_unpaid_orders():
                            self.balance = self.pay_orders()
                            super(Profile, self).save(*args, **kwargs)
        if not hasattr(self, 'cart'):
            from garpix_cart_rest.models import Cart
            super(Profile, self).save(*args, **kwargs)
            Cart.objects.create(profile=self)


    def get_available_for_download(self):
        if self.role == Profile.ROLE.WHOLESALE or (self.role == Profile.ROLE.DROPSHIPPER and hasattr(self, 'profile_shop')):
            return len(Product.get_photos_by_qs(Product.objects.all()))
        elif self.role == Profile.ROLE.DROPSHIPPER and not hasattr(self, 'profile_shop'):
            return 50 - self.download_count
        else:
            return 0

    def set_download_count(self, count):
        self.download_count += count
        self.save()

    def get_unpaid_deliveries(self):
        from garpix_order.models import Delivery
        unpaid_deliveries = Delivery.objects.filter(
            order__in=self.user_orders.filter(status=settings.ORDER_STATUS_DELIVERY_PAYMENT_WAITING))
        return unpaid_deliveries

    def pay_delivery(self):
        from garpix_order.models import Delivery, Order
        balance = self.balance
        deliveries = self.get_unpaid_deliveries()
        for delivery in deliveries.order_by('order__id'):
            if delivery.cost <= balance:
                deliveries.filter(id=delivery.id).update(status=Delivery.STATUS.DELIVERY_PAYMENT_CONFIRMED)
                balance -= delivery.cost
                Order.objects.filter(id=delivery.order.id).update(status=settings.ORDER_STATUS_DELIVERY_PAID)
        return balance

    def get_unpaid_orders(self):
        unpaid_orders = self.user_orders.filter(status=settings.ORDER_STATUS_PAYMENT_WAITING)
        return unpaid_orders

    def pay_orders(self):
        balance = self.balance
        orders = self.get_unpaid_orders()
        for order in orders.order_by('id'):
            if order.order_cost <= balance:
                order_items = order.order_items.all()
                from garpix_order.models import Collection, CollectionItem
                from garpix_catalog.models import Currency, ProductSku

                orders.filter(id=order.id).update(status=settings.ORDER_STATUS_IN_PROCESS)
                order.order_items.all().update(status=settings.ORDER_ITEM_STATUS_PAID)
                if order.profile.role == 2:
                    for order_item in order_items:
                        if order_item.product.product.product_rc.rc_type == 1:
                            status_collection = False
                            product = order_item.product.product
                            collections = Collection.objects.filter(product=product)
                            if collections.count() > 0:
                                for collection in collections:
                                    if collection.product.id == product.id:
                                        collection_items = CollectionItem.objects.filter(collection=collection)
                                        for collection_item in collection_items:
                                            if collection_item.sku == order_item.product and collection_item.order_item == None:
                                                try:
                                                    collection_item.order_item = order_item
                                                    collection_item.redeemed = True
                                                    collection_item.save()
                                                except:
                                                    pass
                                                # new
                                                order_item.status = 'collection'
                                                order_item.save()
                                                status_collection = True
                            else:
                                collection = Collection(product=product)
                                collection.save()
                                sizes = product.product_rc.sizes.all()
                                for size in sizes:
                                    try:
                                        product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                                    except:
                                        product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                        product_sku.save()
                                    collection_item = CollectionItem(collection=collection, sku=product_sku)
                                    collection_item.save()
                                    if product_sku.id == order_item.product.id:
                                        collection_item.redeemed = True
                                        collection_item.order_item = order_item
                                        collection_item.save()
                                        # new
                                        order_item.status = 'collection'
                                        order_item.save()
                                        status_collection = True
                            if status_collection == False:
                                collection = Collection(product=product)
                                collection.save()
                                sizes = product.product_rc.sizes.all()
                                for size in sizes:
                                    try:
                                        product_sku = ProductSku.objects.get(product=product, size=size, color=order_item.product.color)
                                    except:
                                        product_sku = ProductSku(product=product, size=size, color=order_item.product.color)
                                        product_sku.save()
                                    collection_item = CollectionItem(collection=collection, sku=product_sku)
                                    collection_item.save()
                                    if product_sku.id == order_item.product.id:
                                        if order_item.status == 'payment_waiting':
                                            collection_item.redeemed = False
                                        else:
                                            collection_item.redeemed = True
                                            # new
                                            order_item.status = 'collection'
                                            order_item.save()
                                            collection_item.order_item = order_item
                                            collection_item.save()
                                        status_collection = True
                balance -= order.order_cost
        return balance
