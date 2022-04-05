from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path

from ..models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'cost', 'status', 'profile']
    search_fields = [
        'order__id', 'order__order_number',
        'order__profile__user__first_name', 'order__profile__user__middle_name', 'order__profile__user__last_name',
    ]

    change_form_template = 'delivery_payment.html'

    def get_urls(self, *args, **kwargs):
        my_urls = [
            path('<path:pk>/change/delivery_payment/', self.delivery_payment, name='delivery_payment'),
        ]
        return my_urls + super(DeliveryAdmin, self).get_urls(*args, **kwargs)

    def delivery_payment(self, request, pk):
        try:
            instance = self.get_object(request, pk)
            profile = instance.order.profile
            if profile.balance < instance.cost:
                need_to = instance.cost - profile.balance
                self.message_user(request, f"Не хватает {need_to} PLN...", level=messages.DEFAULT_LEVELS['ERROR'])
                return HttpResponseRedirect('../')
            instance.status = instance.STATUS.DELIVERY_PAYMENT_CONFIRMED
            instance.save()
            profile.balance -= instance.cost
            profile.save()
            self.message_user(request, "Оплата заказа подтверждена...", level=messages.DEFAULT_LEVELS['SUCCESS'])
            return HttpResponseRedirect('../')
        except:
            self.message_user(request, "Что-то пошло не так...", level=messages.DEFAULT_LEVELS['ERROR'])
            return HttpResponseRedirect('../')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        instance = self.get_object(request, object_id)
        return super(DeliveryAdmin, self).changeform_view(
            request, object_id, form_url, extra_context={
                'is_show_button': instance.status == 'delivery_payment_waiting'})
