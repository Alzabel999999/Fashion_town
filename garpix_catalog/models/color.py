from django.db import models
from ..mixins.content import OrderingMixin


class Color(OrderingMixin):
    title = models.CharField(max_length=50, verbose_name='Название', blank=False, null=False, default='', unique=True)
    color = models.CharField(max_length=7, verbose_name='Цвет', blank=True, default='')

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ('ordering', 'title')

    def __str__(self):
        return self.title
