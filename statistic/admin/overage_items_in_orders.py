from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import path
from garpix_order.models import OrderItem, Order
from statistic.models import OverageItemsInOrdersStatistic
from statistic.views.registration_statistic import get_time_range_filter
from solo.admin import SingletonModelAdmin


@admin.register(OverageItemsInOrdersStatistic)
class OverageItemsInOrdersStatisticAdmin(SingletonModelAdmin):
    # todo проверить
    change_form_template = 'admin/overage_items_in_orders_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('overage_items_in_orders_statistic/', self.overage_items_in_orders_statistic),
            path('download_doc/', self.download_doc),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to = get_time_range_filter(request)
            all_orders = Order.objects.all() \
                .filter(created_at__gte=datetime_from,
                        created_at__lte=datetime_to,
                        profile__role__in=[1, 2]).count()
            all_items = OrderItem.objects.all(). \
                filter(order__created_at__gte=datetime_from,
                       order__created_at__lte=datetime_to,
                       order__profile__role__in=[1, 2]).count()
            overage = float(all_items / all_orders) if all_orders != 0 else 'Делить на ноль нельзя'
            result = [
                datetime_from,
                datetime_to,
                all_orders,
                all_items,
                overage,
            ]
            return result

    def overage_items_in_orders_statistic(self, request):
        """
        среднее кол-во товаров в посылке (без опта).
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to, all_orders, all_items, overage = self.generate_statistic(request)
            output = [
                {'all_orders': all_orders},
                {'all_items': all_items},
                {'overage': overage},
            ]
            context = {
                'datetime_from': datetime_from,
                'datetime_to': datetime_to,
                'data': output,
            }
            return render(request, 'admin/overage_items_in_orders_statistic.html', context)

    def download_doc(self, request):
        datetime_from, datetime_to, all_orders, all_items, overage = self.generate_statistic(request)
        return OverageItemsInOrdersStatistic.generate_doc(datetime_from,
                                                          datetime_to,
                                                          all_orders,
                                                          all_items,
                                                          overage)
