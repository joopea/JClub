from __future__ import unicode_literals

from classytags.helpers import InclusionTag
from django import template
from form_utils.forms import BetterForm, BetterModelForm
from form_utils.utils import select_template_from_string
from django.conf import settings
from django.utils.translation import get_language

from lib.utils.functions import _get_current_view, _reverse


register = template.Library()


@register.filter
def render_form(form, template_name=None):
    """
    Renders a ``django.forms.Form`` or
    ``form_utils.forms.BetterForm`` instance using a template.

    The template name(s) may be passed in as the argument to the
    filter (use commas to separate multiple template names for
    template selection).

    If not provided, the default template name is
    ``form_utils/form.html``.

    If the form object to be rendered is an instance of
    ``form_utils.forms.BetterForm`` or
    ``form_utils.forms.BetterModelForm``, the template
    ``form_utils/better_form.html`` will be used instead if present.

    """
    default = 'forms/_form.html'
    if isinstance(form, (BetterForm, BetterModelForm)):
        default = ','.join(['forms/_better_form.html', default])
    tpl = select_template_from_string(template_name or default)

    return tpl.render(template.Context({'form': form}))


class SwitchLanguage(InclusionTag):
    template = 'utils/_switch_language.html'

    def get_context(self, context):
        request = context['request']

        current_view, func_name = _get_current_view(request.path)

        urls = []

        for lang_code, description in settings.LANGUAGES:
            url = _reverse(lang_code, current_view, func_name)
            urls.append((url, lang_code, description))

        return {
            'languages': urls,
        }

register.tag(SwitchLanguage)


class SEOLinks(InclusionTag):
    template = 'utils/_seo_links.html'

    def get_context(self, context):
        request = context['request']

        current_view, func_name = _get_current_view(request.path)

        links = []

        current_language = get_language()

        for lang_code, description in settings.LANGUAGES:
            if lang_code == current_language:
                continue

            url = _reverse(lang_code, current_view, func_name)
            links.append((url, lang_code, 'alternate'))

        return {
            'links': links,
        }

register.tag(SEOLinks)
