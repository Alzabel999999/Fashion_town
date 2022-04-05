from django.db import models


class Country(models.Model):
    title = models.CharField(max_length=60, default='', verbose_name='Название', unique=True)
    delivery_price = models.PositiveIntegerField(verbose_name='Цена доставки для розницы')#

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ('title',)

    def __str__(self):
        return self.title
