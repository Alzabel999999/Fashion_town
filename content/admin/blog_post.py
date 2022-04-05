from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from ..models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(TabbedTranslationAdmin):
    pass
