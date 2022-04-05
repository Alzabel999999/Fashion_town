from django.contrib import admin
from ..models.news_rubric import NewsRubric


@admin.register(NewsRubric)
class NewsRubricAdmin(admin.ModelAdmin):
    list_display = ['title', ]
