from django.contrib import admin
from ..models import Announce


@admin.register(Announce)
class AnnounceAdmin(admin.ModelAdmin):
    list_display = ['content', 'url', 'is_active', ]
    fields = ['is_active', 'content', 'background', 'url', 'target_blank', ]
    list_editable = ['is_active']
