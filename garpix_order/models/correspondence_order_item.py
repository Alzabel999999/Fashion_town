from django.db import models
from user.models import User
from . import OrderItem


class CorrespondenceOrderItem(models.Model):
    order_item = models.ForeignKey(OrderItem, blank=True, null=True, verbose_name='Товар заказа',
                              on_delete=models.CASCADE, related_name='correspondence_messages')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='user_correspondence_order_items')
    message = models.TextField(blank=True, default='', verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-id', ]

    def __str__(self):
        return f'{self.order_item}'


    @classmethod
    def create(cls, user, data, files=[]):
        from . import CorrespondenceOrderItemImage
        order_item_id = data.get('order_item_id', None)
        if not order_item_id:
            return False
        order_item = OrderItem.objects.filter(id=order_item_id).first()
        message = data.get('message', '')
        new_correspondence = cls.objects.create(order_item=order_item, user=user, message=message)
        for file in files:
            if 'image' in file.content_type and file.size < 3000000:
                CorrespondenceOrderItemImage.objects.create(correspondence=new_correspondence, image=file)
        return new_correspondence
