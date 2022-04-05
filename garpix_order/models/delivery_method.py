from django.db import models
from django.conf import settings
from garpix_page.abstract.mixins.content import TitleMixin



"""class DeliveryType(TitleMixin):
    title = models.CharField(max_length=100, verbose_name='Название', null=False, blank=False, default='')
    type = models.CharField(max_length=100, choices=settings.CHOICE_DELIVERY_TYPES, unique=True,
                            verbose_name='Тип доставки')

    class Meta:
        verbose_name = 'Тип доставки'
        verbose_name_plural = 'Типы доставки'

    def __str__(self):
        return self.title"""

class DeliveryMethod(TitleMixin):
    #title = models.CharField(max_length=100, verbose_name='Название', null=False, blank=False, default='')
    type = models.CharField(max_length=100, choices=settings.CHOICE_DELIVERY_TYPES, unique=True,
                            verbose_name='Тип доставки')
    #type = models.ForeignKey(DeliveryType, verbose_name='Тип', on_delete=models.SET_NULL,
                                   #blank=False, null=True, related_name='delivery_type')
    class Meta:
        verbose_name = 'Метод доставки'
        verbose_name_plural = 'Методы доставки'

    def __str__(self):
        return self.title
        #return self.type.title
