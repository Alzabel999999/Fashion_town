from django.db import models
from .news import News
from ..mixins.content import VideoMixin, OrderingMixin
from django.conf import settings


class NewsVideo(VideoMixin, OrderingMixin):
    news = models.ForeignKey(News, verbose_name='Новость',
                             related_name='news_videos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ('ordering', '-id')

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
