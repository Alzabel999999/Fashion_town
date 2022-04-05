from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import path
from solo.admin import SingletonModelAdmin
from garpix_order.models import OrderItem
from statistic.models import RevenueSumStatistic
from statistic.views.registration_statistic import get_time_range_filter


@admin.register(RevenueSumStatistic)
class RevenueSumStatisticAdmin(SingletonModelAdmin):
    # todo проверить почему падает
    change_form_template = 'admin/revenue_sum_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('revenue_sum_statistic/', self.revenue_sum_statistic),
            path('download_doc/', self.download_doc),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to = get_time_range_filter(request)

            orders_prices = OrderItem.objects.filter(
                order__created_at__gte=datetime_from,
                order__created_at__lte=datetime_to,
            ).values('price', 'product__product__purchase_price')
            orders_count = OrderItem.objects.filter(
                order__created_at__gte=datetime_from,
                order__created_at__lte=datetime_to,
            ).count()

            list_of_all_prices = []

            list_of_purchase_price = []

            acceptable_values = '0123456789.'

            for price in orders_prices.values('price'):
                num = ''
                for i in str(price):
                    if i not in acceptable_values:
                        str(price).replace(i, '')
                    else:
                        num += i
                list_of_all_prices.append(float(num))
            for price in orders_prices.values('product__product__purchase_price'):
                num = ''
                for i in str(price):
                    if i not in acceptable_values:
                        str(price).replace(i, '')
                    else:
                        num += i
                list_of_purchase_price.append(float(num))
            price_sum = sum(list_of_all_prices)
            purchase_price_sum = sum(list_of_purchase_price)
            revenue = price_sum - purchase_price_sum

            output = [
                datetime_from,
                datetime_to,
                orders_count,
                price_sum,
                purchase_price_sum,
                revenue
            ]
            return output

    def revenue_sum_statistic(self, request):
        """
        Сумма выручки (разница себестоимости и цен продаж за выбранный период)
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to, orders_count, \
            price_sum, purchase_price_sum, revenue = self.generate_statistic(request)
            output = [
                {'orders_count': orders_count},
                {'price': price_sum},
                {'purchase_price': purchase_price_sum},
                {'revenue': revenue},
            ]
            context = {
                'date_from': datetime_from,
                'date_to': datetime_to,
                'data': output,
            }
            return render(request, 'admin/revenue_sum_statistic.html', context)

    def download_doc(self, request):
        datetime_from, datetime_to, orders_count, \
        price_sum, purchase_price_sum, revenue = self.generate_statistic(request)
        return RevenueSumStatistic.generate_doc(datetime_from,
                                                datetime_to,
                                                orders_count,
                                                price_sum,
                                                purchase_price_sum,
                                                revenue)
