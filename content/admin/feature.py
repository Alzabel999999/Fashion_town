from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Feature


@admin.register(Feature)
class FeatureAdmin(TabbedTranslationAdmin):
    pass
