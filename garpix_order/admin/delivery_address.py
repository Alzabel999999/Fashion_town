from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import DeliveryAddress


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'profile', ]
    search_fields = [
        'post_code', 'country__title', 'city', 'street', 'house', 'flat',
        'first_name', 'middle_name', 'last_name',
        'profile__user__first_name', 'profile__user__middle_name', 'profile__user__last_name',
    ]
