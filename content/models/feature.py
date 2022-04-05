from django.db import models

from ..mixins.content import ActiveMixin, ContentMixin, ImageMixin, OrderingMixin, TimeStampMixin, TitleMixin


class Feature(ActiveMixin, ContentMixin, ImageMixin, OrderingMixin, TimeStampMixin, TitleMixin):

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'

        ordering = ['ordering']

    def __str__(self):
        return self.title
