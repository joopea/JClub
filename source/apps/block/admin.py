from django.contrib import admin
from apps.custom_admin.admin import ImprovedRawIdFields

from .models import BlockByCommunity, BlockByUser


class BlockByCommunityAdmin(ImprovedRawIdFields):
    list_display = ['community', 'target', 'created']
    raw_id_fields = ['community', 'target']
    list_filter = ['created']
    search_fields = ['community__name', 'target__username']


class BlockByUserAdmin(ImprovedRawIdFields):
    list_display = ['author', 'target', 'created']
    raw_id_fields = ['author', 'target']
    list_filter = ['created']
    search_fields = ['author__username', 'target__username']

admin.site.register(BlockByCommunity, BlockByCommunityAdmin)
admin.site.register(BlockByUser, BlockByUserAdmin)
