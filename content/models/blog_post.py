from django.db import models
from ..mixins.content import ImageMixin, OrderingMixin
from garpix_page.abstract.models.abstract_page import AbstractBasePageModel
from .tag import Tag


class BlogPost(AbstractBasePageModel, OrderingMixin, ImageMixin):
    tags = models.ManyToManyField(Tag, blank=True, db_index=True, related_name='post_tags', verbose_name='Теги')

    class Meta:
        verbose_name = 'Пост блога'
        verbose_name_plural = 'Посты блога'

        ordering = ['ordering']

    def __str__(self):
        return self.title
