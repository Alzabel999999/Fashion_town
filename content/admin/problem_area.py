from django.contrib import admin
from ..models import ProblemArea


@admin.register(ProblemArea)
class ProblemAreaAdmin(admin.ModelAdmin):
    pass
