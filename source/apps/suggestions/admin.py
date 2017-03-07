from django.contrib import admin
from apps.custom_admin.admin import ImprovedRawIdFields

from .models import HottestPost, PromotedPost, HottestCommunity


class HottestPostAdmin(ImprovedRawIdFields):
    raw_id_fields = ['post']


class PromotedPostAdmin(ImprovedRawIdFields):
    raw_id_fields = ['post']


class HottestCommunityAdmin(ImprovedRawIdFields):
    raw_id_fields = ['community']


admin.site.register(HottestPost, HottestPostAdmin)
admin.site.register(PromotedPost, PromotedPostAdmin)
admin.site.register(HottestCommunity, HottestCommunityAdmin)
