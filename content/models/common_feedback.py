from django.db import models
from django.core.validators import EmailValidator
from .problem_area import ProblemArea


class CommonFeedback(models.Model):

    problem_area = models.ForeignKey(ProblemArea, verbose_name='Проблемная область', on_delete=models.SET_NULL,
                                     related_name='problem_area_feedbacks', blank=True, null=True, default=None)
    name = models.CharField(max_length=256, verbose_name='Имя')
    email = models.CharField(max_length=256, verbose_name='E-mail', validators=[EmailValidator, ])
    message = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Общая обратная связь'
        verbose_name_plural = 'Общая обратная связь'
        ordering = ('-id', )
