from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import DeliveryMethod


@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    pass
