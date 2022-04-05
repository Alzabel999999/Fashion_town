from django.db import models
from . import CorrespondenceOrderItem
from ..mixin import VideoMixin, ImageMixin


class CorrespondenceOrderItemImage(ImageMixin):
    correspondence = models.ForeignKey(
        CorrespondenceOrderItem, blank=True, null=True, verbose_name='Сообщение',
        on_delete=models.CASCADE, related_name='correspondence_order_item_message_images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
