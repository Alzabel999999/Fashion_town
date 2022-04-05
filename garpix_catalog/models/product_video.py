from django.db import models
from ..mixins.content import OrderingMixin, VideoMixin
from ..models import Product


class ProductVideo(OrderingMixin, VideoMixin):
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    product = models.ForeignKey(Product, verbose_name='Товар',
                                related_name='product_videos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ('ordering',)

    def get_video(self):
        from django.conf import settings
        if self.youtube_video:
            return self.youtube_video
        if self.video:
            return settings.SITE_URL + self.video.url
        return '#'

    def get_video_preview(self):
        from django.conf import settings
        if self.video_preview:
            return settings.SITE_URL + self.video_preview.url
        return '#'
