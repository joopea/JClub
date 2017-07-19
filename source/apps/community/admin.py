from django.utils.translation import ugettext_lazy as _
from adminsortable.admin import SortableAdmin
from django.contrib import admin

from .models import Community


class CommunityAdmin(SortableAdmin):
    list_display = ['name', 'description', 'get_post_count', 'created', 'language']
    search_fields = ['name', 'description']

    def get_post_count(self, obj):
        return obj.community_post.count()

    get_post_count.short_description = _('Post Count')


admin.site.register(Community, CommunityAdmin)
