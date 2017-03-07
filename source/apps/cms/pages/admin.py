from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from feincms.admin.item_editor import ItemEditor, FEINCMS_CONTENT_FIELDSET

from apps.cms.pages.models import Page


class PageAdmin(ItemEditor):
    inlines = []

    raw_id_fields = ()
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title']

    fieldsets = (
        ('General', {
            'classes': ('grp-collapse grp-open',),
            'fields': ('title', 'slug')
        }),
        FEINCMS_CONTENT_FIELDSET,
    )


admin.site.register(Page, PageAdmin)
