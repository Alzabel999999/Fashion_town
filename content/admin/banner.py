from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Banner


@admin.register(Banner)
class BannerAdmin(TabbedTranslationAdmin):
    list_display = ['title', 'banner_type', 'url', 'is_active', 'ordering']
    list_editable = ['is_active', 'ordering']
    readonly_fields = ['image_thumb', ]
    fields = ['is_active', 'ordering', 'title', 'banner_type', 'content', 'footnote',
              'image', 'image_thumb', 'url', 'target_blank', 'css_class', ]
