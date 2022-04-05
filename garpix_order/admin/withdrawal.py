from django.contrib import admin
from ..models import Withdrawal


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    search_fields = ['full_name', ]
