from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.text import slugify
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from .color import Color
from .size import Size
from .product import Product
from ..mixins.content import OrderingMixin, ImageMixin
from garpix_utils.file_field import get_file_path


class ProductSku(OrderingMixin, ImageMixin, AbstractBasePageModel):

    title = models.CharField(max_length=255, verbose_name='Название', blank=True, default='')
    product = models.ForeignKey(Product, related_name='product_skus', verbose_name='Товар',
                                on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='size_skus', verbose_name='Размер',
                             on_delete=models.SET_NULL, blank=False, null=True)
    color = models.ForeignKey(Color, related_name='color_skus', verbose_name='Цвет',
                              on_delete=models.SET_NULL, blank=False, null=True)
    in_stock_count = models.PositiveIntegerField(verbose_name='В наличии, шт.', default=0)
    # todo подсчитать количество заказов
    orders_count = models.PositiveIntegerField(verbose_name='Количество заказов, шт.', default=0)
    weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.000,
                                 verbose_name='Вес единицы товара, кг', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Цена',
                                blank=True, null=True)
    is_in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    image = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True,
                             verbose_name='Изображение')

    sites = models.ManyToManyField(
        Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    class Meta:
        verbose_name = 'SKU товара'
        verbose_name_plural = 'SKU товаров'
        unique_together = ['product', 'size', 'color']
        ordering = ('ordering', '-id')

    def __str__(self):
        return f'{self.product.title} {self.size} {self.color}'

    def save(self, *args, **kwargs):
        if self.in_stock_count > 0:
            self.is_in_stock = True
        else:
            self.is_in_stock = False
        self.slug = slugify(self.pk, )
        super(ProductSku, self).save(*args, **kwargs)
        self.product.save()

    def get_conditions(self):
        return {'product_rc': self.product.product_rc, 'brand_rc': self.product.brand.brand_rc}

    def get_price(self, role=0):
        product = self.product
        if role == 3:
            return product.wholesaller_total_price_auto
        elif role == 2:
            return product.dropshipper_total_price_auto
        else:
            return product.retailer_total_price_auto

    def get_image(self):
        if self.image and self.image_thumb:
            return settings.SITE_URL + self.image_thumb
        return self.product.get_image()

    def get_full_image(self):
        if self.image:
            return settings.SITE_URL + self.image.url
        return self.product.get_full_image()

    def get_size(self):
        size = {'id': self.size.id, 'order': self.size.get_size_number(), 'name': self.size.get_size_name()}
        return size

    def get_color(self):
        color = {'id': self.color.id, 'title': self.color.title, 'color': self.color.color}
        return color
