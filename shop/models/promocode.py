from django.db import models
from . import Shop


class Promocode(models.Model):

    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='shop_promocodes', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name='Активность', default=True)
    title = models.CharField(verbose_name='Название', max_length=100)
    discount = models.DecimalField(verbose_name='Скидка, %', max_digits=3, decimal_places=1)
    usage_count = models.PositiveIntegerField(verbose_name='Количество применений промокода', default=0)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
        unique_together = ['shop', 'title']

    def __str__(self):
        return f'{self.shop.title} - {self.title} - {self.discount}%'
