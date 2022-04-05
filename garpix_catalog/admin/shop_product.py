from django.contrib import admin
from ..models import ShopProduct


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):

    list_display = ['__str__', 'shop']
    fieldsets = [
        (None, {'fields': (
            'product', 'shop',
            ('purchase_price', 'recommended_price'), ('price', 'total_price_auto'),
        )}),
        ('SEO', {'fields': ('seo_title', 'seo_keywords', 'seo_description', 'seo_author',
                            'seo_og_type', 'seo_image',), 'classes': ('tabed',)})]
    readonly_fields = ['purchase_price', 'recommended_price', 'total_price_auto']
