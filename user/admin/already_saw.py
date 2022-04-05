from django.contrib import admin
from ..models.already_saw import AlreadySaw


@admin.register(AlreadySaw)
class AlreadySawAdmin(admin.ModelAdmin):
    pass
