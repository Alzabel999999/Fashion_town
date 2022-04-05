from django.contrib import admin
from ..models import ShopConfig


@admin.register(ShopConfig)
class ShopConfigAdmin(admin.ModelAdmin):
    pass
