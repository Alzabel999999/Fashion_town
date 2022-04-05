from django.db import models
from ..mixins.content import OrderingMixin
from ..mixins import ImageMixin
from ..models import Product


class ProductImage(ImageMixin, OrderingMixin):
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    product = models.ForeignKey(Product, verbose_name='Товар',
                                related_name='product_images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('ordering',)
