from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from ..models import Order, OrderItem, CorrespondenceItem
from django_admin_multiple_choice_list_filter.list_filters import MultipleChoiceListFilter



class OrderStatus(MultipleChoiceListFilter):
    title = 'Статус'
    parameter_name = 'status__in'
    def lookups(self, request, model_admin):
        countries = set([c for c in settings.CHOICE_ORDER_STATUSES])
        return [(c) for c in countries]

class OrderItemInline(admin.TabularInline):
    raw_id_fields = ('product', 'cart_item', 'cart_items_pack')
    model = OrderItem
    extra = 0
    exclude = ('extra', )


class CorrespondenceItemInline(admin.TabularInline):
    model = CorrespondenceItem
    show_change_link = True
    extra = 0
    readonly_fields = ['user', 'message']

    def has_add_permission(self, request, obj):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'status', 'order_cost', 'profile', 'created_at', 'updated_at']
    fieldsets = (
        (None, {
            'fields': (
                'profile',
                'order_number', 'slug',
                'status', 'old_status', 'delivery_method', 'payment_method', 'delivery_address', 'parent',
                'services', 'comment', 'track_number', 'specification',
                'order_cost', 'delivery_cost', 'total_services_cost', 'total_cost', 'weight',
            )}),
        ('Получатель', {
            'fields': (
                'first_name', 'middle_name', 'last_name',
            ), 'classes': ('tabed',)}),
        ('ПД получателя', {
            'fields': (
                'passport_number', 'passport_issued', 'passport_issue_date',
            ), 'classes': ('tabed',)}),
    )
    readonly_fields = ['slug', 'order_number', 'order_cost', 'delivery_cost', 'total_services_cost', 'total_cost']
    inlines = (OrderItemInline, CorrespondenceItemInline)
    search_fields = [
        'profile__user__first_name', 'profile__user__middle_name', 'profile__user__last_name',
        'profile__user__username', 'id', 'order_number'
    ]
    list_filter = [OrderStatus, 'created_at', 'updated_at']#['status', 'created_at', 'updated_at']
    raw_id_fields = ['delivery_method', 'delivery_address']#'payment_method'

    def save_related(self, request, form, formsets, change):
        super(OrderAdmin, self).save_related(request, form, formsets, change)
        instance = form.instance
        instance.save()

    change_form_template = 'order_payment.html'

    def get_urls(self, *args, **kwargs):
        my_urls = [
            path('<path:pk>/change/order_payment/', self.order_payment, name='order_payment'),
        ]
        return my_urls + super(OrderAdmin, self).get_urls(*args, **kwargs)

    def order_payment(self, request, pk):
        try:
            instance = self.get_object(request, pk)
            profile = instance.profile
            if profile.balance < instance.total_cost:
                need_to = instance.total_cost - profile.balance
                self.message_user(request, f"Не хватает {need_to} PLN...", level=messages.DEFAULT_LEVELS['ERROR'])
                return HttpResponseRedirect('../')
            instance.status = settings.ORDER_STATUS_IN_PROCESS
            instance.save()
            profile.balance -= instance.total_cost
            profile.save()
            self.message_user(request, "Оплата заказа подтверждена...", level=messages.DEFAULT_LEVELS['SUCCESS'])
            return HttpResponseRedirect('../')
        except:
            self.message_user(request, "Что-то пошло не так...", level=messages.DEFAULT_LEVELS['ERROR'])
            return HttpResponseRedirect('../')

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        instance = self.get_object(request, object_id)
        if instance:
            return super(OrderAdmin, self).changeform_view(
                request, object_id, form_url, extra_context={
                    'is_show_button': instance.status in ['created', 'payment_waiting']})
        return super(OrderAdmin, self).changeform_view(request, object_id, form_url, extra_context)
