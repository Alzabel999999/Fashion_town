from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import path
from solo.admin import SingletonModelAdmin
from app import settings
from garpix_order.models import Order, OrderItem
from statistic.models import OrdersStatusStatistic
from statistic.views.registration_statistic import get_time_range_filter


@admin.register(OrdersStatusStatistic)
class OrdersStatusStatisticAdmin(SingletonModelAdmin):
    # todo проверить
    change_form_template = 'admin/orders_status_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('orders_status_statistic/', self.orders_status_statistic),
            path('download_doc/', self.download_doc),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to = get_time_range_filter(request)
            items_redeemed = OrderItem.objects.filter(
                order__created_at__gte=datetime_from,
                order__created_at__lte=datetime_to,
                status=settings.ORDER_ITEM_STATUS_REDEEMED,
            ).count()
            items_replacement = OrderItem.objects.filter(
                order__created_at__gte=datetime_from,
                order__created_at__lte=datetime_to,
                status=settings.ORDER_ITEM_STATUS_REPLACEMENT,
            ).count()
            orders_closed = Order.objects.filter(
                created_at__gte=datetime_from,
                created_at__lte=datetime_to,
                status=settings.ORDER_STATUS_CLOSED,
            ).count()
            all_orders = Order.objects.all().count()
            all_items = OrderItem.objects.all().count()
            orders_percent = str(float(all_orders / orders_closed)) + '%' \
                if orders_closed != 0 else 'деление на ноль'
            items_redeemed_percent = str(float(all_items / items_redeemed)) + '%' \
                if items_redeemed != 0 else 'деление на ноль'
            items_replacement_percent = str(float(all_items / items_replacement)) + '%' \
                if items_replacement != 0 else 'деление на ноль'

            result = [
                datetime_from,
                datetime_to,
                items_redeemed,
                items_replacement,
                orders_closed,
                orders_percent,
                items_redeemed_percent,
                items_replacement_percent,
            ]
            return result

    def orders_status_statistic(self, request):
        """
        по количеству выкупленных товаров, завершенных заявок, замен и их процентное соотношение.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to, items_redeemed, \
            items_replacement, orders_closed, orders_percent, \
            items_redeemed_percent, items_replacement_percent = self.generate_statistic(request)
            result = [
                {'items_redeemed': items_redeemed},
                {'items_replacement': items_replacement},
                {'orders_closed': orders_closed},
                {'orders_percent': orders_percent},
                {'items_redeemed_percent': items_redeemed_percent},
                {'items_replacement_percent': items_replacement_percent},
            ]
            print(items_redeemed)
            context = {
                'date_from': datetime_from,
                'date_to': datetime_to,
                'data': result
            }
            return render(request, 'admin/orders_status_statistic.html', context)

    def download_doc(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to, items_redeemed, \
            items_replacement, orders_closed, orders_percent, \
            items_redeemed_percent, items_replacement_percent = self.generate_statistic(request)
            return OrdersStatusStatistic.generate_doc(datetime_from,
                                                      datetime_to,
                                                      items_redeemed,
                                                      items_replacement,
                                                      orders_closed,
                                                      orders_percent,
                                                      items_redeemed_percent,
                                                      items_replacement_percent)
