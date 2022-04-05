from django.contrib import admin

from ..models.live_photo_feedback import LivePhotoFeedback


@admin.register(LivePhotoFeedback)
class LivePhotoFeedbackAdmin(admin.ModelAdmin):
    list_display = ('__str__', )
    readonly_fields = ('created_at', )
