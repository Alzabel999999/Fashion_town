from django.db import models


class Service(models.Model):

    title = models.CharField(max_length=128, verbose_name='Название', blank=False, null=False, default='')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    cost = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2, default=0.00)
    for_retail = models.BooleanField(verbose_name='Для розничных покупателей', default=True)
    for_drop = models.BooleanField(verbose_name='Для дроппшиперов', default=True)
    for_opt = models.BooleanField(verbose_name='Для оптовых покупателей', default=True)

    class Meta:
        verbose_name = 'Доп. услуга'
        verbose_name_plural = 'Доп. услуги'
        ordering = ('-id',)

    def __str__(self):
        return self.title
