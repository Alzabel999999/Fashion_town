from django.contrib import admin
from ..models.brand_category import BrandCategory


@admin.register(BrandCategory)
class BrandCategoryAdmin(admin.ModelAdmin):
    list_display = ['brand', 'category', ]
    fieldsets = (
        (None, {'fields': (
            'brand',
            'category',
            'markup_for_retailer',
            'markup_for_dropshipper',
            ('markup_for_wholesaller', 'markup_for_wholesaller_type'),
        )}),
    )
    search_fields = ['brand__title', 'category__title']
