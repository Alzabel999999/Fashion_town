from django.contrib import admin
from ..models.manager import Manager
from ..models.user import User


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
