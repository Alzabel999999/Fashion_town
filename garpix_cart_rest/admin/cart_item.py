from django.contrib import admin
from ..models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'price', 'qty', 'cart', 'status']
    raw_id_fields = ['product', ]
    readonly_fields = ['total_price', 'old_price', 'pack', 'price', 'discount', 'status']

    def get_queryset(self, request):
        qs = super(CartItemAdmin, self).get_queryset(request).filter(pack=None)
        # qs = super(CartItemAdmin, self).get_queryset(request)
        return qs
