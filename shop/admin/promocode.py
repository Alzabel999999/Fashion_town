from django.contrib import admin
from ..models import Promocode


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_active', 'usage_count']
    list_editable = ['is_active', ]
