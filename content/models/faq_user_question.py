from django.db import models
from django.core.validators import EmailValidator
from .question_category import QuestionCategory


class FAQUserQuestion(models.Model):

    name = models.CharField(max_length=256, verbose_name='ФИО')
    email = models.CharField(max_length=256, verbose_name='E-mail', validators=[EmailValidator, ])
    category = models.ForeignKey(QuestionCategory, verbose_name='Категория', related_name='category_questions',
                                 blank=True, null=True, default=None, on_delete=models.SET_NULL)
    question = models.TextField(verbose_name='Вопрос')

    class Meta:
        verbose_name = 'Вопрос от пользователя'
        verbose_name_plural = 'Вопросы от пользователей'
        ordering = ('-id', )
