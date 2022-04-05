from django.db import models
from shop.models import Shop


class ShopRequisites(models.Model):

    requisites = models.TextField(verbose_name='Реквизиты', blank=True, default='')
    shop = models.OneToOneField(Shop, verbose_name='Магазин', related_name='shop_requisites',
                                on_delete=models.CASCADE, blank=False, null=False, default=None)

    class Meta:
        verbose_name = 'Реквизиты магазина'
        verbose_name_plural = 'Реквизиты магазинов'

    def __str__(self):
        title = str(self.requisites).split('\n')[0]
        return f'{title}... ({self.shop})'
