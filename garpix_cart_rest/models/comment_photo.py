from django.db import models
from .cart_item_comment import CartItemComment
from ..mixins.content import ImageMixin, OrderingMixin


class CartItemCommentPhoto(ImageMixin, OrderingMixin):
    comment = models.ForeignKey(CartItemComment, verbose_name='Комментарий',
                                related_name='cart_item_comment_photos', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ('ordering', '-id')
