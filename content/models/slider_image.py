from django.db import models
from ..mixins.content import ContentAsTextMixin, ImageMixin, OrderingMixin, TitleMixin
from ..models import Slider


class SliderImage(ImageMixin, TitleMixin, ContentAsTextMixin, OrderingMixin):
    slider = models.ForeignKey(Slider, verbose_name='Слайдер', on_delete=models.CASCADE)
    url = models.CharField(max_length=1000, blank=True, verbose_name='URL', default='/')

    class Meta:
        verbose_name = 'Изображение слайдера'
        verbose_name_plural = 'Изображения слайдера'

        ordering = ['ordering']

    def __str__(self):
        return self.title
