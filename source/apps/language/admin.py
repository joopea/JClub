from django.contrib import admin
from apps.custom_admin.admin import ImprovedRawIdFields
from .models import Language


class LanguageAdmin(ImprovedRawIdFields):
    list_display = ['name', 'initial', 'status']
    search_fields = ['name']


admin.site.register(Language, LanguageAdmin)
