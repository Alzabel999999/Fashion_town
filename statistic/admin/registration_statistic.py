import datetime
import urllib
from django.contrib import admin
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import path
from solo.admin import SingletonModelAdmin
from statistic.models.registration_statistic import RegistrationStatistic
from statistic.views.registration_statistic import get_time_range_filter
from user.models import Profile


@admin.register(RegistrationStatistic)
class RegistrationStatisticAdmin(SingletonModelAdmin):
    change_form_template = 'statistic/registration_statistic.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.registration_statistic),
        ]
        return my_urls + urls

    def generate_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        else:
            date_from = request.POST.get('date_from', None)
            if date_from in [None, '']:
                date_from = datetime.date(2021, 1, 1)
            if type(date_from) == type(str()):
                date_from = datetime.datetime.strptime(date_from, '%Y-%m-%dT%H:%M').date()
            date_to = request.POST.get('date_to', datetime.datetime.now().date())
            if date_to in [None, '']:
                date_to = datetime.datetime.now().date()
            if type(date_to) == type(str()):
                date_to = datetime.datetime.strptime(date_to, '%Y-%m-%dT%H:%M').date()
            retailers_count = Profile.objects.filter(
                user__date_joined__gte=date_from,
                user__date_joined__lte=date_to,
                role=1,
                user__status=3
            ).count()

            dropshippers_count = Profile.objects.filter(
                user__date_joined__gte=date_from,
                user__date_joined__lte=date_to,
                role=2,
                user__status=3
            ).count()

            wholesaler_count = Profile.objects.filter(
                user__date_joined__gte=date_from,
                user__date_joined__lte=date_to,
                role=3,
                user__status=3
            ).count()
            result = [
                date_from,
                date_to,
                wholesaler_count,
                dropshippers_count,
                retailers_count
            ]
            return result

    def registration_statistic(self, request):
        if not request.user.is_superuser:
            return HttpResponseForbidden('403')
        datetime_from, datetime_to, retailers_count, dropshippers_count, wholesaler_count = self.generate_statistic(request)
        if '_registration_statistic' in request.POST:
            output = [
                {'role': 'Розничных покупателей', 'count': retailers_count},
                {'role': 'Дропшипперов', 'count': dropshippers_count},
                {'role': 'Оптовых покупателей', 'count': wholesaler_count}
            ]
            context = {
                'date_from': datetime_from,
                'date_to': datetime_to,
                'str_date_from': datetime.datetime.strftime(datetime_from, '%Y-%m-%dT00:00'),
                'str_date_to': datetime.datetime.strftime(datetime_to, '%Y-%m-%dT00:00'),
                'data': output,
            }
            return render(request, 'statistic/registration_statistic.html', context)
        elif '_registration_statistic_doc' in request.POST:
            return RegistrationStatistic.generate_doc(datetime_from,
                                                      datetime_to,
                                                      retailers_count,
                                                      dropshippers_count,
                                                      wholesaler_count)
        else:
            return render(request, 'statistic/registration_statistic.html', {})
