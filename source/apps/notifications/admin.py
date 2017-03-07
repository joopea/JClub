from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from apps.custom_admin.admin import ImprovedRawIdFields, ReadOnlyTabularInline

from .models import Notification


class NotificationAdmin(ImprovedRawIdFields):
    date_hierarchy = 'created'
    raw_id_fields = ['author', 'owner', ]
    fields = ['subject', 'author', 'owner', 'relation_1', 'original']
    list_display = ['subject', 'is_warning', 'get_original', 'author', 'owner', 'created']
    search_fields = ['subject', 'author__username', 'author__username']
    list_filter = ['subject', 'created']

    def is_warning(self, obj):
        return obj.is_warning

    is_warning.boolean = True

    def get_original(self, obj):
        return obj.original or ''

    get_original.short_description = _("Message")


admin.site.register(Notification, NotificationAdmin)


class AlertsInline(ReadOnlyTabularInline):
    model = Notification
    extra = 0
    fk_name = 'owner'
    can_delete = True

    def get_queryset(self, request):
        qs = super(AlertsInline, self).get_queryset(request)
        return qs.filter(subject__in=Notification.WARNING_TYPES)
