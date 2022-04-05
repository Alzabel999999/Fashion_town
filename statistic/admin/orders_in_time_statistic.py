from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import path
from solo.admin import SingletonModelAdmin
from garpix_order.models import Order
from statistic.models import OrdersInTimeStatistic
from statistic.views.registration_statistic import get_time_range_filter


@admin.register(OrdersInTimeStatistic)
class OrdersInTimeStatisticAdmin(SingletonModelAdmin):
    # todo проверить
    change_form_template = 'admin/orders_in_time_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('orders_in_time_statistic/', self.orders_in_time_statistic),
            path('download_doc/', self.download_doc),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to = get_time_range_filter(request)
            wholesalers = []
            dropshippers = []
            retailers = []
            usernames = []
            data = Order.objects.filter(
                created_at__gte=datetime_from,
                created_at__lte=datetime_to,
                profile__role__in=[1, 2, 3]
            ).prefetch_related(
                'order_items__product__product__brand',
                'profile__user',
            )
            for user in data.values('profile__user__username'):
                user = str(user.values())
                user = user[14:-3]
                if user in usernames:
                    pass
                else:
                    usernames.append(user)
                    brands = []
                    user_brands = []
                    for brand in data.filter(
                            profile__user__username=user).values(
                        'order_items__product__product__brand__title'):
                        title = str(brand.values())
                        title = title[14:-3]
                        if title not in brands and title != 'on':
                            brands.append(title)
                            user_brands.append(
                                {
                                    'title': title,
                                    'count': data.filter(
                                        profile__user__username=user,
                                        order_items__product__product__brand__title=title,
                                    ).count()
                                }
                            )
                    for role in data.filter(profile__user__username=user).values('profile__role'):
                        role = str(role.values())
                        role = role[13:-2]
                        if role == '1':
                            retailers.append(
                                {
                                    'nickname': user,
                                    'brands': user_brands,
                                    'orders': data.filter(
                                        profile__user__username=user
                                    ).count()
                                }
                            )
                            break
                        elif role == '2':
                            dropshippers.append(
                                {
                                    'nickname': user,
                                    'brands': user_brands,
                                    'orders': data.filter(
                                        profile__user__username=user
                                    ).count()
                                }
                            )
                            break
                        else:
                            wholesalers.append(
                                {
                                    'nickname': user,
                                    'brands': user_brands,
                                    'orders': data.filter(
                                        profile__user__username=user
                                    ).count()
                                }
                            )
                            break
        result = [
            datetime_from,
            datetime_to,
            wholesalers,
            dropshippers,
            retailers
        ]
        return result

    def orders_in_time_statistic(self, request):
        """
        Статистика по общему количеству заказов (период, фирма, логины, категории пользователей).
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to, wholesalers, dropshippers, retailers = self.generate_statistic(request)

            context = {
                'date_from': datetime_from.strftime('%Y-%m-%d'),
                'date_to': datetime_to.strftime('%Y-%m-%d'),
                'wholesalers': wholesalers,
                'dropshippers': dropshippers,
                'retailers': retailers
            }
            return render(request, 'admin/orders_in_time_statistic.html', context)

    def download_doc(self, request):
        datetime_from, datetime_to, wholesalers, dropshippers, retailers = self.generate_statistic(request)
        return OrdersInTimeStatistic.generate_doc(datetime_from,
                                                  datetime_to,
                                                  wholesalers,
                                                  dropshippers,
                                                  retailers)
