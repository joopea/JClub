from django.contrib import admin

from .models import Wall


class WallAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wall, WallAdmin)
