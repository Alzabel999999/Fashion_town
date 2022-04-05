from django.db import models
from django.conf import settings
from garpix_page.abstract.mixins.content import TitleMixin


class PaymentMethod(TitleMixin):
    type = models.CharField(max_length=100, choices=settings.CHOICE_PAYMENT_TYPES, unique=True,
                            verbose_name='Тип оплаты') #unique=True,

    class Meta:
        verbose_name = 'Метод оплаты'
        verbose_name_plural = 'Методы оплаты'

    def __str__(self):
        return self.title
