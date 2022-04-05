from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from solo.admin import SingletonModelAdmin
from garpix_order.models import Order
from statistic.models import OrdersPerCityStatistic


@admin.register(OrdersPerCityStatistic)
class OrdersPerCityStatisticAdmin(SingletonModelAdmin):
    # todo проверить
    change_form_template = 'admin/orders_per_city_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('orders_per_city_statistic/', self.orders_per_city_statistic),
            path('download_doc/', self.download_doc),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            city_orders_count = {}
            for citys in Order.objects.all().values('delivery_address__city'):
                for city in citys.values():
                    city_orders_count[city] = Order.objects.filter(delivery_address__city=city).count()
            return city_orders_count

    def orders_per_city_statistic(self, request):
        """
        Статистика по количеству заказов в каждом городе
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            city_orders_count = self.generate_statistic(request)
            context = {
                'data': city_orders_count.items(),
            }
            return render(request, 'admin/orders_per_city_statistic.html', context)

    def download_doc(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            city_orders_count = self.generate_statistic(request)
            return OrdersPerCityStatistic.generate_doc(citys=city_orders_count.keys(),
                                                       counts=city_orders_count.values())
