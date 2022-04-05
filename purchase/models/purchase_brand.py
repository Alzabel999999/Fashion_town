from django.db import models


class PurchaseBrand(models.Model):

    def title(self): pass
    title.short_description = 'Бренд'

    def ordered_in_brand(self): pass
    ordered_in_brand.short_description = 'Количество заказов'

    def condition(self): pass
    condition.short_description = 'Условие выкупа'

    def producer(self): pass
    producer.short_description = 'Производство'

    class Meta:
        verbose_name = 'Закупки по бренду'
        verbose_name_plural = 'Закупки по брендам'
