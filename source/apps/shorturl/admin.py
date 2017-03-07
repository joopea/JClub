'''
Created on May 19, 2015

@author: jvdijken
'''
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from apps.shorturl.models import ShortURL
from django.db.models.fields import UUIDField

class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('short', 'long', 'ttl', 'active')
    list_editable = ('ttl', 'active', 'long')
    readonly_fields = ('short', )


admin.site.register(ShortURL, ShortURLAdmin)
