from django.contrib import admin
from ..models import ShopCategoryMarkup


@admin.register(ShopCategoryMarkup)
class ShopCategoryMarkupAdmin(admin.ModelAdmin):

    list_display = ['shop', 'category', 'markup']
