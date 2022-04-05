from django.db import models
#from garpix_order.models import Order
from django.contrib import admin


class PurchaseOrder(models.Model):#models.Model
    #order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL)

    def order_number(self): pass
    order_number.short_description = 'Номер заказа'

    def items_count(self): pass
    items_count.short_description = 'Количество товаров в заказе'


    def status(self): pass
    status.short_description = 'Статус'
    #status.admin_order_field = 'Статус'


    class Meta:
        verbose_name = 'Закупки по заказу'
        verbose_name_plural = 'Закупки по заказам'
