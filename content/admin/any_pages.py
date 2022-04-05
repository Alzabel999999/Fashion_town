from django.contrib import admin
from solo.admin import SingletonModelAdmin
from ..models.any_pages import AnyPages


@admin.register(AnyPages)
class AnyPagesAdmin(SingletonModelAdmin):
    fieldsets = (
        ('Регистрация / авторизация', {'fields': ('auth_reg_image', 'auth_reg_text')}),
    )
