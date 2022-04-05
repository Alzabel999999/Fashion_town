from django.db import models
from .news import News
from ..mixins.content import ImageMixin, OrderingMixin


class NewsPhoto(ImageMixin, OrderingMixin):
    news = models.ForeignKey(News, verbose_name='Новость',
                             related_name='news_photos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('ordering', '-id')
