from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    fieldsets = (
        (None, {'fields': ('title', 'slug', 'is_active', 'ordering', 'content', 'parent', 'page_type',)}),
        ('SEO', {'fields': ('seo_title', 'seo_keywords', 'seo_description', 'seo_author',
                            'seo_og_type', 'seo_image',), 'classes': ('tabed',)})
    )
    readonly_fields = ('slug',)
    list_display = ('tree_actions', 'indented_title', 'ordering')
    ordering = ('title',)
