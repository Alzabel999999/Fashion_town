from django.contrib import admin
from ..models import CartItem, CartItemsPack


class CartItemInline(admin.TabularInline):
    raw_id_fields = ['product', ]
    model = CartItem
    extra = 0


@admin.register(CartItemsPack)
class CartItemsPackAdmin(admin.ModelAdmin):
    inlines = (CartItemInline, )
    raw_id_fields = ['product', ]
    readonly_fields = [
        'color', 'size', 'condition', 'in_pack_count', 'total_count', 'price', 'old_price', 'total_price', 'status']
    list_display = ['product', 'total_price', 'qty', 'in_pack_count', 'total_count', 'cart', 'status']
