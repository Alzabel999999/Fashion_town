from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils.timezone import now, datetime
from rest_framework.viewsets import GenericViewSet, ViewSet

from garpix_catalog.models import Brand, ProductSku
from garpix_order.models import Order
from user.models import User, Profile


def get_time_range_filter(request):
    """
    Функция для определения дат начала и конца периода в зависимотси от параметров запроса.
    """
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)

    if not date_from:
        datetime_to = now()
        datetime_from = datetime(year=2020, month=1, day=1, tzinfo=datetime_to.tzinfo)
    else:
        datetime_to = datetime.strptime(date_to, '%d-%m-%Y')  # + timedelta(hours=23, minutes=59, seconds=59)
        datetime_from = datetime.strptime(date_from, '%d-%m-%Y')

    return datetime_from, datetime_to


def get_brand_filter(request):
    title = request.GET.get('Brand name', None)
    if not title:
        brands = Brand.objects.all()
    else:
        brands = Brand.objects.filter(title=title)
    return brands


def get_username_filter(request):
    username = request.GET.get('username', None)
    if not username:
        users = User.objects.all()
    else:
        users = User.objects.filter(username=username)
    return users


def get_role_filter(request):
    role = request.GET.get('role', None)

    if not role:
        roles = Profile.role
    else:
        roles = Profile.objects.filter(role=role)
    return roles


def get_user_status_filter(request):
    status = request.GET.get('user_status', None)
    if not status:
        output = User.objects.all()
    else:
        output = User.objects.filter(status=status)
    return output


def get_orders_count(request):
    orders_count = request.GET.get('orders', None)
    if not orders_count:
        output = ProductSku.objects.all()
    else:
        # pass
        output = ProductSku.objects.filter(orders_count=orders_count)
    return output


class RegisterStatistic(GenericViewSet, ViewSet):
    def register_statistic(self, request):

        if not request.user.is_staff:
            return HttpResponseForbidden('403')
        else:
            datetime_from, datetime_to = get_time_range_filter(request)

            user_register = request.GET.get('user', 0)
            user_role = request.GET.get('role', 0)

            users = User.objects.filter(register_at__gte=datetime_from,
                                        created_at__lte=datetime_to)
            # roles = Profile.objects.filter(register_at__gte=datetime_from,
            #                                created_at__lte=datetime_to)

            if user_register and user_register != 0:
                users = users.filter(user=user_register)
            if user_role and user_role != 0:
                users = users.filter(role=user_role)

            result = {}
            for user in users:
                result[user.keys] = user

            context = {
                'date_from': datetime_from.strftime('%Y-%m-%dT%H:%M'),
                'date_to': datetime_to.strftime('%Y-%m-%dT%H:%M'),
                'users': result,
            }
            return render(request, 'admin/registration_statistic.html', context)
