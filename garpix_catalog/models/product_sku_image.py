from django.db import models
from ..mixins.content import OrderingMixin
from ..mixins import ImageMixin
from ..models import ProductSku


class ProductSkuImage(ImageMixin, OrderingMixin):
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    product_sku = models.ForeignKey(ProductSku, verbose_name='SKU Товара',
                                    related_name='product_sku_images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('ordering',)
