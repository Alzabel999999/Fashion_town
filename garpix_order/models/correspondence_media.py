from django.db import models
from . import CorrespondenceItem
from ..mixin import VideoMixin, ImageMixin


class CorrespondenceImage(ImageMixin):
    correspondence = models.ForeignKey(
        CorrespondenceItem, blank=True, null=True, verbose_name='Сообщение',
        on_delete=models.CASCADE, related_name='correspondence_message_images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class CorrespondenceVideo(VideoMixin):
    correspondence = models.ForeignKey(
        CorrespondenceItem, blank=True, null=True, verbose_name='Сообщение',
        on_delete=models.CASCADE, related_name='correspondence_message_videos')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
