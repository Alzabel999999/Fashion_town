from django.core.exceptions import ValidationError
from django.db import models
from shop.models import Shop
from . import Category


def validate_zero(value):
    if value == 0:
        raise ValidationError('0')


class ShopCategoryMarkup(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', related_name='category_markups',
                                 on_delete=models.CASCADE, default=None)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='shop_markups',
                             on_delete=models.CASCADE, default=None)
    markup = models.DecimalField(max_digits=10, decimal_places=2,
                                 null=False, blank=False, default='0.00',
                                 verbose_name='Наценка на категорию')

    class Meta:
        verbose_name = 'Наценка на категорию'
        verbose_name_plural = 'Наценки на категории'
        ordering = ('-id', )

    def save(self, *args, **kwargs):
        super(ShopCategoryMarkup, self).save(*args, **kwargs)
        [product.save() for product in self.get_products()]

    def get_products(self):
        return self.shop.shop_products.filter(product__category=self.category)
