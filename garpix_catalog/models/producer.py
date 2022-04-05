from garpix_page.abstract.mixins.content import ActiveMixin, ContentMixin, TimeStampMixin, TitleMixin
from ..mixins.content import ImageMixin, OrderingMixin


class Producer(ActiveMixin, ImageMixin, OrderingMixin, TimeStampMixin, TitleMixin):

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

        ordering = ['ordering']

    def __str__(self):
        return self.title
