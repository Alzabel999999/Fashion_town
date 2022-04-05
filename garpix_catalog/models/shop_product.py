from decimal import Decimal
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db import models
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from shop.models import Shop
from .product import Product
from .shop_category_markup import ShopCategoryMarkup
from ..mixins.content import OrderingMixin


def validate_zero(value):
    if value == 0:
        raise ValidationError('0')


class ShopProduct(OrderingMixin, AbstractBasePageModel):

    product = models.ForeignKey(Product, verbose_name='Товар', related_name='product_shop_products',
                                on_delete=models.CASCADE, default=None)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='shop_products',
                             on_delete=models.CASCADE, default=None)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_zero, ],
                                         null=False, blank=False, default='0.00',
                                         verbose_name='Закупочная цена')
    recommended_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_zero, ],
                                            null=False, blank=False, default='0.00',
                                            verbose_name='Рекомендованная цена')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                null=True, blank=True, default='0.00',
                                verbose_name='Новая цена')
    total_price_auto = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_zero, ],
                                null=False, blank=False, default='0.00',
                                verbose_name='Итоговая цена (авто)')
    sites = models.ManyToManyField(Site, verbose_name='Сайты для отображения', default=settings.SITE_ID, blank=True)

    class Meta:
        verbose_name = 'Товар магазина'
        verbose_name_plural = 'Товары магазинов'
        ordering = ('ordering', '-id')
        unique_together = ('product', 'shop')

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        product = self.product
        self.purchase_price = product.dropshipper_total_price_auto
        self.recommended_price = product.retailer_total_price_auto
        if self.price and self.price != 0:
            self.total_price_auto = self.price
        else:
            markup = self.get_markup()
            if markup and markup != 0:
                self.total_price_auto = product.dropshipper_total_price_auto + markup
            else:
                self.total_price_auto = product.retailer_total_price_auto
        super(ShopProduct, self).save(*args, **kwargs)

    def get_markup(self):
        markup = ShopCategoryMarkup.objects.filter(shop=self.shop, category=self.product.category).first()
        if markup:
            return markup.markup
        return None

    def get_price(self, currency=Decimal('1.00')):
        return self.total_price_auto * currency

    @classmethod
    def get_products_in_shop_qs(cls, shop_id):
        return Product.objects.filter(product_shop_products__shop__id=shop_id).distinct()

    @classmethod
    def get_products_not_in_shop_qs(cls, shop_id):
        return Product.objects.exclude(product_shop_products__shop__id=shop_id).distinct()

    @classmethod
    def get_shop_product(cls, shop_id, product_id):
        return cls.objects.filter(shop__id=shop_id, product__id=product_id).first()

    @classmethod
    def create(cls, shop, data):
        product_id = data.get('product_id', None)
        price = data.get('price', Decimal('0.00'))
        if product_id:
            cls.objects.create(
                shop=shop,
                product=Product.objects.filter(id=product_id).first(),
                price=price,
            )
            return True
        return False
