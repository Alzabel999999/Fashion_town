from django.db import models
from django.db.models import Count, Q
from garpix_catalog.models import RedemptionCondition, Product
from django.dispatch import receiver
import time

class Collection(models.Model):

    class STATUS:
        IN_COLLECTION = 0
        COLLECTED = 1
        TYPES = (
            (IN_COLLECTION, 'В процессе сбора'),
            (COLLECTED, 'Сбор завершен'),
        )

    product = models.ForeignKey(Product, verbose_name='Товар', related_name='product_collections',
                                blank=False, null=False, default=None, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(verbose_name='Статус', choices=STATUS.TYPES, default=STATUS.IN_COLLECTION)

    class Meta:
        verbose_name = 'Сбор'
        verbose_name_plural = 'Сборы'
        ordering = ['status', '-id', ]

    def __str__(self):
        return f'Сбор №{self.id} ({self.product.title})'

    '''
python backend/manage.py shell -c "from garpix_order.models.collection import Collection"
from garpix_order.models import Collection, OrderItem
order_item = OrderItem.objects.first()
Collection.create_collection(order_item=order_item)
    '''
    @classmethod
    def create_collection(cls, order_item):

        from ..models import CollectionItem

        product_sku = order_item.product
        product = product_sku.product
        condition = product.get_condition()
        collection = Collection.objects.create(product=product)
        other_skus = product_sku.product.get_skus_by_condition(size=product_sku.size, color=product_sku.color)

        for sku in other_skus:
            for n in range(condition.number):
                CollectionItem.objects.create(
                    collection=collection,
                    sku=sku,
                    redeemed=False,
                )
        item = collection.collection_items.filter(sku=product_sku).first()
        item.redeemed = True
        item.order_item = order_item
        item.save()

        return collection

    '''
python backend/manage.py shell -c "from garpix_order.models.collection import Collection"
from garpix_order.models import Collection, OrderItem
order_item = OrderItem.objects.last()
Collection.add_to_some_collection(order_item=order_item)
    '''
    @classmethod
    def add_to_some_collection(cls, order_item):

        from ..models import CollectionItem

        if hasattr(order_item, 'order_item_collection_item'):
            return None

        item = CollectionItem.objects.annotate(collection_redeemed_items_count=Count(
            'collection', filter=Q(collection__collection_items__redeemed=True))).filter(
            redeemed=False, order_item=None, sku=order_item.product, collection__status=0).order_by(
            '-collection_redeemed_items_count', 'id').first()
        if item:
            item.redeemed = True
            item.order_item = order_item
            item.save()
            return item.collection
        else:
            return cls.create_collection(order_item)

    @classmethod
    def get_collections(cls, product, color=None):
        from garpix_catalog.models import Color
        if color:
            color = Color.objects.filter(id=color).first()
        else:
            color = product.product_skus.first().color
        collections = cls.objects.filter(product=product, collection_items__sku__color=color).distinct()
        return collections

    def get_items_rows(self):
        from garpix_catalog.models import Size
        condition_number = self.product.get_condition().number
        color = self.collection_items.first().sku.color
        skus = self.product.product_skus.filter(color=color)
        sizes = Size.objects.filter(size_skus__in=skus).distinct()
        items = self.collection_items.all()
        result = []
        for cn in range(condition_number):
            row = []
            for size in sizes:
                row.append(list(items.filter(sku__size=size))[cn])
            result.append(row)
        return result

    @classmethod
    def create_fake_empty_collection(cls, product_data):
        from garpix_catalog.models import ProductSku
        from ..models import CollectionItem
        product_id = product_data.get('product', None)
        size_id = product_data.get('size', None)
        color_id = product_data.get('color', None)
        if not product_id or not size_id or not color_id:
            return False
        product_sku = ProductSku.objects.filter(product__id=product_id, size__id=size_id, color__id=color_id).first()
        product = product_sku.product
        condition = product.get_condition()
        collection = Collection.objects.create(product=product)
        other_skus = product.get_skus_by_condition(size=product_sku.size, color=product_sku.color)
        for sku in other_skus:
            for n in range(condition.number):
                CollectionItem.objects.create(
                    collection=collection,
                    sku=sku,
                    redeemed=False,
                )
        return collection

@receiver(models.signals.post_save, sender=Collection)
def check_condition_collection(sender, instance, using, **kwargs):
    from ..models.collection_item import CollectionItem
    #collection = instance
    #sizes = collection.product.product_rc.sizes.all()
    #collection_items = collection.collection_items.all()
    #collection_items_redeemed = collection.collection_items.all().filter(redeemed=True)
    #if collection.status == 1 and len(collection_items_redeemed) == len(sizes):
        #for collection_item in collection_items:
            #collection_item.order_item.status = 'paid'
            #collection_item.order_item.save()
    collection_items = CollectionItem.objects.filter(collection=instance)
    if instance.status == 1:
        #time.sleep(4)
        for collection_item in collection_items:
            collection_item.order_item.status = 'paid'
            collection_item.order_item.save()
