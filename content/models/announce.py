from django.db import models
from django.conf import settings
from garpix_page.abstract.mixins.content import ActiveMixin, ContentMixin, TimeStampMixin, TitleMixin
from ..mixins.content import ImageMixin, OrderingMixin
from garpix_utils.file_field import get_file_path


class Announce(ContentMixin):
    url = models.CharField(max_length=1000, blank=True, verbose_name='URL', default='/')
    target_blank = models.BooleanField(default=False, verbose_name='Открывать в новом окне')
    background = models.FileField(max_length=255, upload_to=get_file_path, default='', blank=True, verbose_name='Фон')
    is_active = models.BooleanField(verbose_name='Включено', default=True)

    class Meta:
        verbose_name = 'Анонс'
        verbose_name_plural = 'Анонсы'
        ordering = ('-id',)

    def __str__(self):
        return self.url
