from django.db import models
from django.utils.safestring import mark_safe


class PurchaseProduct(models.Model):

    def purchase_title(self): pass
    purchase_title.short_description = 'Название'

    def purchase_size(self): pass
    purchase_size.short_description = 'Размер'

    def purchase_color(self): pass
    purchase_color.short_description = 'Цвет'

    def purchase_brand(self): pass
    purchase_brand.short_description = 'Бренд'

    def purchase_order(self): pass
    purchase_order.short_description = 'Заказ'

    def purchase_image(self, obj):
        return mark_safe('<img src={{obj.image.url}} />')
    purchase_image.short_description = 'Превью'


    class Meta:
        verbose_name = 'Закупки по товару'
        verbose_name_plural = 'Закупки по товарам'
