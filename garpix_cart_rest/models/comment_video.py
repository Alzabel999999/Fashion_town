from django.db import models
from .cart_item_comment import CartItemComment
from ..mixins.content import VideoMixin, OrderingMixin


class CartItemCommentVideo(VideoMixin, OrderingMixin):
    comment = models.ForeignKey(CartItemComment, verbose_name='Комментарий',
                                related_name='cart_item_comment_videos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'
        ordering = ('ordering', '-id')
