from django.contrib import admin
from ..models.notification import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
