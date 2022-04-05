from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from ..models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'profile', 'name', 'cost', 'receipt', 'created_at', 'updated_at', 'status']
    fields = ['profile', 'name', 'cost', 'comment', 'receipt', 'status', 'requisites', 'created_at', 'updated_at', ]
    # readonly_fields = ['status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    search_fields = [
        'order__id', 'delivery__order__id', 'order__order_number', 'delivery__order__order_number',
        'order__profile__user__first_name', 'order__profile__user__middle_name', 'order__profile__user__last_name',
        'delivery__order__profile__user__first_name', 'delivery__order__profile__user__middle_name',
        'delivery__order__profile__user__last_name',
    ]

    change_form_template = 'confirm_payment.html'

    def get_urls(self, *args, **kwargs):
        my_urls = [
            path('<path:pk>/change/confirm_payment/', self.confirm_payment, name='confirm_payment'),
        ]
        return my_urls + super(PaymentAdmin, self).get_urls(*args, **kwargs)

    def confirm_payment(self, request, pk):
        try:
            instance = self.get_object(request, pk)
            instance.status = instance.STATUS.SUCCESSFULLY
            instance.save()
            profile = instance.profile
            profile.balance += instance.cost
            profile.save()
            self.message_user(request, "Оплата подтверждена...", level=messages.DEFAULT_LEVELS['SUCCESS'])
            instance.set_order_in_process_status()
            from user.models import Notification
            notification = Notification(profile=profile, message='Ваш баланс пополнен на {0} PLN . Благодарим за сотрудничество!'.format(instance.cost))
            notification.save()
            #self.message_user(request, str(inst), level=messages.DEFAULT_LEVELS['SUCCESS'])
            return HttpResponseRedirect('../')
        except Exception as e:
            #self.message_user(request, str(e), level=messages.DEFAULT_LEVELS['SUCCESS'])
            self.message_user(request, "Что-то пошло не так...", level=messages.DEFAULT_LEVELS['ERROR'])
            return HttpResponseRedirect('../')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id:
            instance = self.get_object(request, object_id)
            return super(PaymentAdmin, self).changeform_view(
                request, object_id, form_url, extra_context={'is_show_button': instance.status == instance.STATUS.EXPECTED})
        return super(PaymentAdmin, self).changeform_view(request, object_id, form_url, extra_context)
