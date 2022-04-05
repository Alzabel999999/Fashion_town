from django.db import models


class QuestionCategory(models.Model):

    category = models.CharField(max_length=256, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория вопроса'
        verbose_name_plural = 'Категории вопросов'
        ordering = ('-id', )

    def __str__(self):
        return f'{self.category}'
