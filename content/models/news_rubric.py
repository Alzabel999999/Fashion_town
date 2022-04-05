from django.db import models


class NewsRubric(models.Model):

    title = models.CharField(max_length=255, verbose_name='Название', default='', unique=True)

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('title',)

    def __str__(self):
        return self.title
