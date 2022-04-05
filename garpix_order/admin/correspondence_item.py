from django.contrib import admin
from ..models import CorrespondenceItem, CorrespondenceImage, CorrespondenceVideo


class CorrespondenceImageInLine(admin.TabularInline):
    model = CorrespondenceImage
    extra = 0


class CorrespondenceVideoInLine(admin.TabularInline):
    model = CorrespondenceVideo
    extra = 0


@admin.register(CorrespondenceItem)
class CorrespondenceItemAdmin(admin.ModelAdmin):
    inlines = [CorrespondenceImageInLine, CorrespondenceVideoInLine]
    search_fields = [
        'order__id', 'order__order_number',
        'user__username', 'user__first_name', 'user__middle_name', 'user__last_name',
    ]
    list_display = ['user', 'order']
    readonly_fields = ['user', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        return super(CorrespondenceItemAdmin, self).save_model(request, obj, form, change)
