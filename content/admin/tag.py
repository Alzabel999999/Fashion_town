from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Tag


@admin.register(Tag)
class TagAdmin(TabbedTranslationAdmin):
    pass
