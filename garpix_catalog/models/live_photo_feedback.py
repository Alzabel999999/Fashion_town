from django.db import models
from . import LivePhotoImage, LivePhotoVideo
from datetime import datetime


class LivePhotoFeedback(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name="Никнейм или email", default='')
    message = models.TextField(verbose_name="Сообщение", blank=True, default='')
    media_photo = models.ForeignKey(LivePhotoImage, verbose_name='Фото', related_name='live_photo_photo_feedbacks',
                                    blank=True, null=True, on_delete=models.CASCADE)
    media_video = models.ForeignKey(LivePhotoVideo, verbose_name='Видео', related_name='live_photo_video_feedbacks',
                                    blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Создано', default=datetime.now)

    class Meta:
        verbose_name = "Запрос с живых фото"
        verbose_name_plural = "Запросы с живых фото"
        ordering = ('created_at',)

    def __str__(self):
        return f'Запрос от {self.name} - {self.created_at}'
