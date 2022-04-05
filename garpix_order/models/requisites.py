from django.db import models
import random

class Requisites(models.Model):
    requisites = models.TextField(verbose_name='Реквизиты', blank=True, default='')

    class Meta:
        verbose_name = 'Реквизиты'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return str(self.requisites).split('\n')[0]

    @classmethod
    def random_requisites(cls):
        return random.choice(cls.objects.all())
