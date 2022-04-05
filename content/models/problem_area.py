from django.db import models


class ProblemArea(models.Model):

    problem_area = models.CharField(max_length=256, verbose_name='Проблемная область')

    class Meta:
        verbose_name = 'Проблемная область'
        verbose_name_plural = 'Проблемные области'
        ordering = ('-id', )

    def __str__(self):
        return f'{self.problem_area}'
