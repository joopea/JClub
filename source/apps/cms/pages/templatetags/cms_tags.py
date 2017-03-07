from django import template
from apps.cms.pages.data_views import PageDataView

register = template.Library()


@register.inclusion_tag('pages/_page_nav.html')
def render_page_nav():

    return {
        'pages': PageDataView.get_pages(),
    }

