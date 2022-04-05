from django.contrib import admin
from ..models import Color
from ..forms import ColorAdminForm


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    form = ColorAdminForm
    list_display = ('title', 'color')
