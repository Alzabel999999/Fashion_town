from django.contrib import admin
from ..models.requisites import Requisites


@admin.register(Requisites)
class RequisitesAdmin(admin.ModelAdmin):
    pass
