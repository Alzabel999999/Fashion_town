from django.contrib import admin
from ..models import Brand, BrandCategory, Product


class BrandCategoryInline(admin.TabularInline):
    model = BrandCategory
    show_change_link = 'title'
    view_on_site = False
    fields = ['category', ]
    readonly_fields = ['category', ]
    extra = 0


class ProductInline(admin.TabularInline):
    model = Product
    show_change_link = 'title'
    view_on_site = False
    fields = ['category', ]
    readonly_fields = ['category', ]
    extra = 0


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'brand_rc', 'is_active', 'producer', 'sertificate']
    list_editable = ['is_active', 'sertificate']
    inlines = [BrandCategoryInline, ProductInline]
    search_fields = ['title', ]
    list_filter = ['sertificate', 'producer']
