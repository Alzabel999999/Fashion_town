from django.contrib import admin
from ..models import Size


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass
