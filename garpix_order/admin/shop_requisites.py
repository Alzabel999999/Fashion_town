from django.contrib import admin
from ..models import ShopRequisites


@admin.register(ShopRequisites)
class ShopRequisitesAdmin(admin.ModelAdmin):
    pass
