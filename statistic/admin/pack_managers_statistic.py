from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import path
from solo.admin import SingletonModelAdmin
from app import settings
from garpix_order.models import Order, OrderItem
from ..models import PackManagersStatistic
from statistic.views.registration_statistic import get_time_range_filter
from user.models import User


@admin.register(PackManagersStatistic)
class PackManagersStatisticAdmin(SingletonModelAdmin):
    # todo сделать
    pass
