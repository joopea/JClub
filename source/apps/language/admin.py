from django.contrib import admin
from apps.custom_admin.admin import ImprovedRawIdFields
from .models import Language

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'initial', 'status']
    search_fields = ['name']
    list_editable = ['status']
    list_filter = ['status']


admin.site.register(Language, LanguageAdmin)
