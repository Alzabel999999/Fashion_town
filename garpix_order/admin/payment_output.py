from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path
from ..models import PaymentOutput


@admin.register(PaymentOutput)
class PaymentOutputAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'profile', 'name', 'number', 'bank', 'cost', 'receipt', 'created_at', 'updated_at']
    fields = ['profile', 'name', 'cost', 'receipt', 'created_at', 'updated_at', 'number', 'bank', ]
    # readonly_fields = ['status', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
