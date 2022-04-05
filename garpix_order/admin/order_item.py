from django.contrib import admin
from ..models import OrderItem, OrderItemCommentPhoto
from django.utils.safestring import mark_safe


class OrderItemCommentPhotoInline(admin.TabularInline):
    model = OrderItemCommentPhoto
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'brand', 'status', 'profile']
    search_fields = [
        'order__profile__user__first_name', 'order__profile__user__middle_name', 'order__profile__user__last_name',
        'order__profile__user__username', 'order__id', 'order__order_number'
    ]
    inlines = [OrderItemCommentPhotoInline, ]
    list_filter = ['status']
    readonly_fields = ["preview"]
    def preview(self, obj):
        new_obj = OrderItemCommentPhoto.objects.get(order_item=obj)
        return mark_safe(f'<img src="{new_obj.image.url}">')
