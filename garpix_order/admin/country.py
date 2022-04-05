from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass
