from django.contrib import admin
from ..models import QuestionCategory


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    pass
