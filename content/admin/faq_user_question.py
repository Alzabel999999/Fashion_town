from django.contrib import admin
from ..models import FAQUserQuestion


@admin.register(FAQUserQuestion)
class FAQUserQuestionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'category', 'question']
