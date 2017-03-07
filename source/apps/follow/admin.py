from django.contrib import admin
from .models import FollowUser, FollowCommunity


class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(FollowUser, FollowAdmin)
admin.site.register(FollowCommunity, FollowAdmin)
