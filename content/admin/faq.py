from django.contrib import admin
from ..models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['answer', 'ordering']
    list_editable = ['ordering', ]
