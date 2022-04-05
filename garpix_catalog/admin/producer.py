from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Producer


@admin.register(Producer)
class ProducerAdmin(TabbedTranslationAdmin):
    pass
