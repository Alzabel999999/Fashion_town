from django.db import models
from django.conf import settings
from garpix_page.abstract.mixins.content import ActiveMixin, ContentMixin, TimeStampMixin, TitleMixin
from ..mixins.content import ImageMixin, OrderingMixin


class Banner(ActiveMixin, ContentMixin, ImageMixin, OrderingMixin, TimeStampMixin, TitleMixin):
    url = models.CharField(max_length=1000, blank=True, verbose_name='URL', default='/')
    target_blank = models.BooleanField(default=False, verbose_name='Открывать в новом окне')
    css_class = models.CharField(max_length=1000, blank=True, verbose_name='Дополнительный класс CSS', default='')
    banner_type = models.CharField(max_length=100, choices=settings.CHOICE_BANNER_TYPES,
                                   verbose_name='Тип баннера', default='')
    footnote = models.CharField(max_length=1000, blank=True, verbose_name='Сноска', default='')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'
        ordering = ('ordering', '-id')

    def __str__(self):
        return self.title
