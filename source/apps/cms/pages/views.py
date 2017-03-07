from django.views.generic.detail import DetailView

from apps.cms.pages.models import Page
from apps.menu.views import WithUserMenu


class PageDetailView(WithUserMenu, DetailView):
    template_name = 'pages/page_detail.html'

    model = Page
