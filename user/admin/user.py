from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
from ..models.user import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'phone', 'status', 'role']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'status', 'first_name', 'middle_name', 'last_name', 'email', 'phone',
                'password_reset_key', 'phone_change_key', 'email_confirmation_key', 'is_email_confirmed')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_buyer', 'is_shop_buyer', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['username', ]
        return []

    # add_form_template = 'admin/auth/user/add_form.html'
    # add_form = UserCreationForm
    # readonly_fields = ('referral', 'get_number_agent', 'get_referral_link')
    # fieldsets = (
    #    ('Дополнительно', {
    #        'fields':
    #            (
    #                 'phone',
    #                 'is_phone_confirmed',
    #                 'phone_confirmation_key',
    #                 'new_phone',
    #                 'email_confirmation_key',
    #                 'is_email_confirmed',
    #                 'new_email',
    #                 'agency',
    #                 'consortia',
    #                 'host_agency',
    #                 'show_agency_statements',
    #                 'type',
    #                 'get_number_agent',
    #                 'rating',
    #                 'bonus_comission',
    #                 'get_referral_link',
    #                 'notify_period',
    #                 'notify_email',
    #                 'is_support',
    #                 'have_to_change_password',
    #                 'last_change_password',
    #                 'statement_period'
    #            )
    #         }
    #     ),
    # ) + UserAdmin.fieldsets
    #
    # list_filter = (
    #     'type',
    # ) + UserAdmin.list_filter
    #
    # list_display = UserAdmin.list_display + (
    #     'get_number_agent',
    # )
