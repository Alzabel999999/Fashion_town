from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse
from django.urls import path
from solo.admin import SingletonModelAdmin
from app import settings
from garpix_order.models import Order, OrderItem
from ..models import UserShopsStatistic
from statistic.views.registration_statistic import get_time_range_filter
from user.models import User


@admin.register(UserShopsStatistic)
class UserShopsStatisticAdmin(SingletonModelAdmin):
    # todo сделать
    pass
