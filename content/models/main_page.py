from django.db import models
from solo.models import SingletonModel
from ..mixins.content import ImageMixin
from garpix_catalog.models import Category


class MainPage(SingletonModel, ImageMixin):
    title = models.CharField(max_length=255, verbose_name='Заголовок', blank=True, default='FASHION TOWN')
    overtitle = models.TextField(verbose_name='Надзаголовок', blank=True,
                                 default='Торговая бизнес-платформа для розничных, оптовых покупателей и дропшипперов')
    undertitle = models.TextField(verbose_name='Подзаголовок', blank=True,
                                  default='Для тех, кто хочет не только покупать, но и зарабатывать!')
    filters = models.ManyToManyField(Category, verbose_name='Фильтры', default=None, blank=True,
                                     related_name='main_page_filters')

    in_stock_product_filters = models.ManyToManyField(
        Category, verbose_name='Фильтры товаров "в наличии"', default=None, blank=True,
        related_name='main_page_in_stock_filters')

    def __str__(self):
        return 'Главная страница'

    class Meta:
        verbose_name = 'Главная страница'
