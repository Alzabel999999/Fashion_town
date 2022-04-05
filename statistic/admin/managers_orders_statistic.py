from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import path
from solo.admin import SingletonModelAdmin
from app import settings
from garpix_order.models import Order, OrderItem
from statistic.models import ManagersOrdersStatistic
from statistic.views.registration_statistic import get_time_range_filter
from user.models import User


@admin.register(ManagersOrdersStatistic)
class ManagersOrdersStatisticAdmin(SingletonModelAdmin):
    pass

    # change_form_template = 'admin/managers_orders_statistic.html'
    #
    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path('managers_orders_statistic/', self.managers_orders_statistic),
    #     ]
    #     return my_urls + urls
    #
    # def managers_orders_statistic(self, request):
    #     """
    #     по каждому из менеджеров сколько единиц выкуплено/упаковано и совокупно
    #     """
    #     if not request.user.is_superuser:
    #         return HttpResponseForbidden('403')
    #     else:
    #         datetime_from, datetime_to = get_time_range_filter(request)
    #         staff_items_redeemed = User.objects.filter(
    #             is_staff=True
    #         )
    #         items_redeemed = OrderItem.objects.filter(
    #             order__created_at__gte=datetime_from,
    #             order__created_at__lte=datetime_to,
    #             status=settings.ORDER_ITEM_STATUS_REDEEMED,
    #             # order__profile__username=user_name,
    #             order__profile__user__is_staff=True,
    #         ).count()
    #         orders_packed = Order.objects.filter(
    #             status=settings.ORDER_STATUS_SENDED,
    #             # profile__username=user_name,
    #             profile__user__is_staff=True,
    #         )
    #         print(staff_items_redeemed)
    #         return HttpResponse(staff_items_redeemed)
