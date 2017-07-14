from django.contrib import admin
from django.contrib.auth import get_user_model
from django import db
from django.db.models import Count
from apps.custom_admin.admin import ReadOnlyTabularInline, ReadOnlyAdmin
from apps.notifications.admin import AlertsInline
from apps.users.forms import UsernameForm
from apps.users.models import UsernameVariation, Username, SecurityQuestion
from lib.users.base_admin import BaseUserAdmin
from lib.users.mixins import AsSULoginMixin
from django.utils.translation import ugettext_lazy as _

from apps.notifications.queries import NotificationDataView

UserModel = get_user_model()


class UserAdmin(AsSULoginMixin, BaseUserAdmin):

    inlines = [AlertsInline]

    list_display = (BaseUserAdmin.username_field, 'is_staff', 'is_superuser', 'show_alerts', 'language')

    fieldsets = (
        (None, {
            'fields': (
                BaseUserAdmin.username_field,
                'password'
            )}),
        ('Personal data', {
            'fields': (
                'language',
                'profile_colour'
            )}),
        ('Authorisation', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
                'last_login',
                'date_joined'
            )}),
    )
    search_fields = (BaseUserAdmin.username_field, )

    def get_readonly_fields(self, request, obj=None):
        read_only = []

        if request.user.is_staff:
            read_only = ['is_superuser', 'user_permissions', 'username', 'password', 'language']
            if not request.user.groups.filter(name='Manager').exists():
                read_only.append('groups')

        if request.user.is_superuser:
            read_only = []  # override
        return list(self.readonly_fields) + read_only

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def show_alerts(self, obj):
        return NotificationDataView.get_alert_count(obj)

    show_alerts.short_description = _("Alerts")

class UsernameVariantAdmin(ReadOnlyAdmin):
    list_display = ['username', 'username_variation', 'username_variation_no']
    search_fields = ['username', 'username_variation']


class UsernameAdmin(admin.ModelAdmin):
    list_display = ['username', 'active']
    list_editable = ['active']
    fields = (('username', 'active'),)
    form = UsernameForm
    search_fields = ['username']
    list_filter = ['active']


class SecurityQuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserModel, UserAdmin)
admin.site.register(Username, UsernameAdmin)
admin.site.register(UsernameVariation, UsernameVariantAdmin)
admin.site.register(SecurityQuestion, SecurityQuestionAdmin)
