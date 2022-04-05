from django.db import models
from ..mixin import ImageMixin


class OrderItemCommentPhoto(ImageMixin):

    order_item = models.ForeignKey('OrderItem', verbose_name='Товар заказа', related_name='order_item_comment_photos',
                                   on_delete=models.SET_NULL, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Фото комментария к товару в заказе'
        verbose_name_plural = 'Фото комментариев товаров в заказах'
