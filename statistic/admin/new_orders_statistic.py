from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.urls import path
from solo.admin import SingletonModelAdmin
from garpix_order.models import Order
from statistic.models import NewOrdersStatistic
from datetime import date
from dateutil.relativedelta import relativedelta


@admin.register(NewOrdersStatistic)
class NewOrdersStatisticAdmin(SingletonModelAdmin):
    # todo проверить
    change_form_template = 'statistic/new_users_orders_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.new_users_orders_statistic),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        """
        по количеству заказов новых пользователей (зарегистрированных до 3 месяцев),
        должны отображаться логины таких пользователей, их категории (Опт, дроп, Розница)
         и данные этих пользователей.
        """
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            datetime_from = date.today() + relativedelta(months=-3)
            datetime_to = date.today()

            wholesalers = {}
            dropshippers = {}
            retailers = {}
            data = Order.objects.filter(
                created_at__gte=datetime_from,
                created_at__lte=datetime_to,
                profile__user__status=3,
                profile__role__in=[1, 2, 3]
            ).prefetch_related(
                'order_items__product__product__brand',
                'profile__user',
            )
            for user in data.values('profile__user__username'):
                user = str(user.values())
                user = user[14:-3]
                counts = data.filter(profile__user__username=user).count()
                for role in data.filter(profile__user__username=user).values('profile__role'):
                    role = str(role.values())
                    role = role[13:-2]
                    if role == '1':
                        retailers[user] = counts
                    elif role == '2':
                        dropshippers[user] = counts
                    else:
                        wholesalers[user] = counts

            result = [
                datetime_from,
                datetime_to,
                wholesalers,
                dropshippers,
                retailers
            ]
            return result

    def new_users_orders_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        datetime_from, datetime_to, wholesalers, dropshippers, retailers = self.generate_statistic(request)
        if '_new_users_orders_statistic' in request.POST or request.method == 'GET':
            context = {
                'date_from': datetime_from,
                'date_to': datetime_to,
                'wholesalers': wholesalers.items(),
                'dropshippers': dropshippers.items(),
                'retailers': retailers.items()
            }
            return render(request, 'statistic/new_users_orders_statistic.html', context)
        elif '_new_users_orders_statistic_doc' in request.POST:
            return NewOrdersStatistic.generate_doc(datetime_from=datetime_from,
                                                   datetime_to=datetime_to,
                                                   wholesalers=wholesalers.items(),
                                                   dropshippers=dropshippers.items(),
                                                   retailers=retailers.items())
        else:
            return render(request, 'statistic/new_users_orders_statistic.html', {})
