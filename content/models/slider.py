from django.db import models
from django.conf import settings
from ..mixins.content import TitleMixin


class Slider(TitleMixin):
    slider_type = models.CharField(max_length=100, choices=settings.CHOICE_SLIDER_TYPES,
                                   verbose_name='Тип слайдера', default='')

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'

        ordering = ['title']

    def __str__(self):
        return self.title
