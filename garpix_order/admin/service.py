from django.contrib import admin
from ..models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'cost', 'for_retail', 'for_drop', 'for_opt', 'description']
    list_editable = ['for_retail', 'for_drop', 'for_opt']
