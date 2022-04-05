from django.db import models
from ..mixins.content import OrderingMixin


class FAQ(OrderingMixin):

    answer = models.CharField(max_length=512, verbose_name='Вопрос')
    question = models.TextField(verbose_name='Ответ')

    class Meta:
        verbose_name = 'Вопрос/Ответ'
        verbose_name_plural = 'Вопросы/Ответы'
        ordering = ('ordering', '-id')

    def __str__(self):
        return self.answer
