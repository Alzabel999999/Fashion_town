from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import PaymentMethod


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    pass
