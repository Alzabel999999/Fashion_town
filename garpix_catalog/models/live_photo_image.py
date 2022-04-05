from django.db import models
from ..mixins.content import OrderingMixin, ImageMixin
from ..models import LivePhotoAlbum


class LivePhotoImage(ImageMixin, OrderingMixin):
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    album = models.ForeignKey(LivePhotoAlbum, verbose_name='Товар', on_delete=models.CASCADE,
                              related_name='live_photo_photos')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('ordering',)
