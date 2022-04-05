from django.contrib import admin
from ..models import Cart, CartItem, CartItemsPack


class CartItemInline(admin.TabularInline):
    raw_id_fields = ['product', ]
    model = CartItem
    extra = 0
    show_change_link = '__str__'
    fields = [
        'product',
        'status', 'change_agreement', 'selected',
        'qty', 'price', 'total_item_price', 'total_price', 'old_price', 'discount'
    ]
    readonly_fields = ['status', ]

    def get_queryset(self, request):
        qs = super(CartItemInline, self).get_queryset(request).filter(pack=None)
        return qs


class CartItemsPackInline(admin.TabularInline):
    raw_id_fields = ['product', ]
    model = CartItemsPack
    extra = 0
    show_change_link = '__str__'
    fields = [
        'product', 'color', 'size', 'condition',
        'status', 'change_agreement', 'selected',
        'qty', 'in_pack_count', 'total_count',
        'price', 'old_price', 'total_price', 'discount'
    ]
    readonly_fields = ['status', 'condition']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = (CartItemInline, CartItemsPackInline)
