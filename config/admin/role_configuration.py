from django.contrib import admin
from ..models.role_configuration import RoleConfiguration


@admin.register(RoleConfiguration)
class RoleConfigurationAdmin(admin.ModelAdmin):
    pass
