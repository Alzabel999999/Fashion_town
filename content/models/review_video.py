from django.db import models
from garpix_utils.file_field import get_file_path
from .review import Review
from ..mixins.content import VideoMixin, OrderingMixin
from django.conf import settings


class ReviewVideo(VideoMixin, OrderingMixin):
    review = models.ForeignKey(Review, verbose_name='Отзыв',
                               related_name='review_videos', on_delete=models.CASCADE)

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

    def save(self, *args, **kwargs):
        super(ReviewVideo, self).save()
        self.review.save()

    def delete(self, using=None, keep_parents=False):
        super(ReviewVideo, self).delete()
        self.review.save()
