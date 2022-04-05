from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Slider
from ..models import SliderImage


class SliderImageInline(admin.TabularInline):
    model = SliderImage
    extra = 0


@admin.register(Slider)
class SliderAdmin(TabbedTranslationAdmin):
    inlines = (SliderImageInline, )
