from django.db import models
from .category import Category
from .brand import Brand


class BrandCategory(models.Model):

    class MURKUP_TYPE:
        PERCENT = 1
        PLN = 2
        TYPES = (
            (PERCENT, '%'),
            (PLN, 'PLN'),
        )

    category = models.ForeignKey(Category, verbose_name='Категория', default='',
                                 blank=True, on_delete=models.CASCADE, related_name='category_brand_categories')
    brand = models.ForeignKey(Brand, verbose_name='Бренд', default='', blank=True, on_delete=models.CASCADE,
                              related_name='brand_brand_categories')

    markup_for_wholesaller = models.DecimalField(
        verbose_name='Наценка для оптовика', max_digits=10, decimal_places=2, blank=True, default=0.00)
    markup_for_wholesaller_type = models.PositiveIntegerField(
        verbose_name='Единицы измерения (доступные значения - PLN или %)', blank=False, null=False, choices=MURKUP_TYPE.TYPES, default=MURKUP_TYPE.PLN)
    markup_for_dropshipper = models.DecimalField(
        verbose_name='Наценка для дроппшипера', max_digits=10, decimal_places=2, blank=True, default=0.00)
    markup_for_retailer = models.DecimalField(
        verbose_name='Розничная наценка', max_digits=10, decimal_places=2, blank=True, default=0.00)

    class Meta:
        verbose_name = 'Категория бренда'
        verbose_name_plural = 'Категории брендов'
        unique_together = ['category', 'brand']
        ordering = ('brand', 'category')

    def __str__(self):
        return f'{self.category} производителя {self.brand}'
