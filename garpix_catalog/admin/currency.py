from django.contrib import admin
from ..models.currency import Currency
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['title', 'ratio']
    change_list_template = "admin/currency_list.html"
    side_bar_on = True

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('update_currencies/', self.update_currencies),
        ]
        return my_urls + urls

    def update_currencies(self, request):
        if "_update_currencies" in request.POST:
            try:
                Currency.get_currencies_from_bank()
            except Exception as e:
                self.message_user(request, f"Что то пошло не так. Ошибка: {str(e)}",
                                  level=messages.DEFAULT_LEVELS['ERROR'])
        return HttpResponseRedirect("../")
