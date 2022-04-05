from django.contrib import admin
from ..models.wishlist_item import WishListItem


@admin.register(WishListItem)
class WishListItemAdmin(admin.ModelAdmin):
    pass
