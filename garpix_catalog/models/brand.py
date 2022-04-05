from django.db import models
from django.db.models import Count
from garpix_utils.file_field import get_file_path


class BrandManager(models.Manager):
    def get_queryset(self):
        return super(BrandManager, self).get_queryset().annotate(
            products_count=Count('brand_products')).exclude(products_count=0)


class Brand(models.Model):

    class PRODUCER:
        POLAND = 1
        IMPORT = 2
        TYPES = (
            (POLAND, 'Польша'),
            (IMPORT, 'Импорт'),
        )

    title = models.CharField(max_length=255, verbose_name='Название', blank=True, default='')
    is_active = models.BooleanField(default=True, verbose_name='Доступен для выбора')
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    image = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True, verbose_name='Изображение')
    brand_rc = models.ForeignKey('RedemptionCondition', related_name='rc_brands', verbose_name='Условие выкупа',
                                 on_delete=models.SET_NULL, blank=True, null=True, default=None)
    sertificate = models.BooleanField(default=False, verbose_name='Сертификат')
    producer = models.PositiveIntegerField(default=PRODUCER.POLAND, choices=PRODUCER.TYPES,
                                           verbose_name='Производитель')

    objects = models.Manager()
    objects_with_products = BrandManager()

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_condition(self):
        return self.brand_rc

    def ordered_in_brand(self):
        items_count = self.get_ordered_products().count()
        packs_count = self.get_ordered_packs().count()
        total_count = packs_count + items_count
        return total_count

    def condition(self):
        return self.brand_rc

    def get_ordered_products(self):
        from garpix_order.models import OrderItem
        return OrderItem.objects.filter(cart_item__product__product__brand=self)

    def get_ordered_packs(self):
        from garpix_order.models import OrderItem
        return OrderItem.objects.filter(cart_items_pack__product__brand=self)
