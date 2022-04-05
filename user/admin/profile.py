from django.contrib import admin

from ..models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'balance', 'passive_balance']

    fieldsets = (
        ('Личная информация', {'fields': ('user', 'role', 'balance')}),
        ('Паспортные данные', {'fields': ('passport_number', 'passport_issued', 'passport_issue_date')}),
        ('Организация', {'fields': ('inn', 'organization')}),
        ('Ссылки', {'fields': ('vk_link', 'insta_link', 'other_link', 'site_link')}),
    )

    #readonly_fields = ('role', )

    search_fields = ['user__first_name', 'user__middle_name', 'user__last_name', 'user__username']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            fieldsets = (
                ('Личная информация', {'fields': ('user', )}),
            )
            return fieldsets

        if obj.role == 3:
            fieldsets = (
                ('Личная информация', {'fields': ('user', 'role', 'balance')}),
                ('Паспортные данные', {'fields': ('passport_number', 'passport_issued', 'passport_issue_date')}),
                ('Организация', {'fields': ('inn', 'organization')}),
                ('Ссылки', {'fields': ('vk_link', 'insta_link', 'other_link', 'site_link')}),
            )
            return fieldsets
        elif obj.role == 2:
            fieldsets = (
                ('Личная информация', {'fields': ('user', 'role', 'balance')}),
                ('Паспортные данные', {'fields': ('passport_number', 'passport_issued', 'passport_issue_date')}),
                ('Ссылки', {'fields': ('vk_link', 'insta_link', 'other_link', 'site_link')}),
                (None, {'fields': ('download_count', )})
            )
            return fieldsets
        else:
            fieldsets = (
                ('Личная информация', {'fields': ('user', 'role', 'balance')}),
                ('Паспортные данные', {'fields': ('passport_number', 'passport_issued', 'passport_issue_date')}),
            )
            return fieldsets
