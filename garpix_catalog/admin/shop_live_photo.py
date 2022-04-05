from django.contrib import admin
from ..models import ShopLivePhoto


@admin.register(ShopLivePhoto)
class ShopLivePhotoAdmin(admin.ModelAdmin):
    pass
