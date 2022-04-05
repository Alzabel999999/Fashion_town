from django.db import models
from ..mixins.content import OrderingMixin, VideoMixin
from ..models import LivePhotoAlbum
from django.conf import settings


class LivePhotoVideo(VideoMixin, OrderingMixin):
    description = models.TextField(verbose_name='Описание', blank=True, default='')
    album = models.ForeignKey(LivePhotoAlbum, verbose_name='Товар', on_delete=models.CASCADE,
                              related_name='live_photo_videos')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ('ordering',)

    def get_video(self):
        if self.youtube_video:
            return self.youtube_video
        if self.video:
            return settings.SITE_URL + self.video.url
        return '#'

    def get_video_preview(self):
        if self.video_preview:
            return settings.SITE_URL + self.video_preview.url
        return '#'
