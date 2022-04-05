from django.db import models
from user.models import User
from . import Order


class CorrespondenceItem(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, verbose_name='Заказ',
                              on_delete=models.CASCADE, related_name='correspondence_messages')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name='Пользователь', on_delete=models.CASCADE,
                             related_name='user_correspondence_items')
    message = models.TextField(blank=True, default='', verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-id', ]

    def __str__(self):
        return f'{self.order}'

    @classmethod
    def create(cls, user, data, files=[]):
        from . import CorrespondenceImage, CorrespondenceVideo
        order_id = data.get('order', None)
        if not order_id:
            return False
        order = Order.objects.filter(id=order_id).first()
        message = data.get('message', '')
        new_correspondence = cls.objects.create(order=order, user=user, message=message)
        for file in files:
            if 'image' in file.content_type and file.size < 3000000:
                CorrespondenceImage.objects.create(correspondence=new_correspondence, image=file)
            if 'video' in file.content_type and file.size < 5000000:
                CorrespondenceVideo.objects.create(correspondence=new_correspondence, video=file)
        return new_correspondence
