from django.contrib import admin
from ..models import CommonFeedback, CommonFeedbackAttachment


class CommonFeedbackAttachmentInline(admin.TabularInline):
    model = CommonFeedbackAttachment
    extra = 0


@admin.register(CommonFeedback)
class CommonFeedbackAdmin(admin.ModelAdmin):
    list_display = ['problem_area', 'name', 'email', 'message']
    inlines = [CommonFeedbackAttachmentInline, ]
