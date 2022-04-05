from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=512, verbose_name='Название тега', default='Tag')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.title
