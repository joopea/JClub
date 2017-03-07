from django.views.generic import ListView

from apps.core.views import ExtraFormDataMixin
from apps.menu.views import WithUserMenu

from .queries import CommunityDataView


class CommunityListView(WithUserMenu, ListView):
    template_name = 'community/list.html'
    queryset = CommunityDataView
    paginate_by = 20

    def get_queryset(self):
        return self.queryset.list()


class WithCommunity(ExtraFormDataMixin):
    def get_extra_data(self, *args, **kwargs):
        context = super(WithCommunity, self).get_extra_data(*args, **kwargs)
        context['community'] = self.kwargs['pk']
        return context
