from collections import OrderedDict

from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string


class Translatable(object):
    def translations(self, obj):
        translations = OrderedDict()

        for lang_code, description in settings.LANGUAGES:
            translations[lang_code] = None

        for trans in obj.translations.all():
            translations[trans.language_code] = trans

        app_label = self.version_model._meta.app_label
        model_name = self.version_model._meta.model_name

        context = {
            'parent': self.get_parent(obj),
            'change_url': 'admin:{0}_{1}_change'.format(app_label, model_name),
            'add_url': 'admin:{0}_{1}_add'.format(app_label, model_name),

            'translations': translations,
        }

        return render_to_string('admin/pages/_translations.html', context)

    def get_parent(self, obj):
        return obj


class RedirectTranslationMixin(object):
    def parent_description(self, obj):
        return obj.parent.description

    def response_add(self, request, obj, post_url_continue="../%s/"):
        if not '_continue' in request.POST:
            return self._parent_changelist_redirect(obj)
        else:
            return super(RedirectTranslationMixin, self).response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if not '_continue' in request.POST:
            return self._parent_changelist_redirect(obj)
        else:
            return super(RedirectTranslationMixin, self).response_change(request, obj)


    def _parent_changelist_redirect(self, obj):
        app_label = self._get_parent(obj)._meta.app_label
        model_name = self._get_parent(obj)._meta.object_name.lower()

        url_name = 'admin:{0}_{1}_changelist'.format(app_label, model_name)

        return HttpResponseRedirect(reverse(url_name))

    def _get_parent(self, obj):
        return obj.parent


class Polymorphic(object):
    def get_changeform_initial_data(self, request):
        initial = super(Polymorphic, self).get_changeform_initial_data(request)

        initial['content_type'] = ContentType.objects.get_for_model(self.model)

        return initial


class PolymorphicVersion(Polymorphic, RedirectTranslationMixin):
    pass


class PageAdmin(Translatable, Polymorphic, admin.ModelAdmin):
    pass
