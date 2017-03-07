from django.views.generic import TemplateView

from apps.menu.views import WithUserMenu

from .queries import SuggestionsQuery


class SuggestionListView(WithUserMenu, TemplateView):
    template_name = 'suggestions/detail.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SuggestionListView, self).get_context_data(**kwargs)
        context['suggestions'] = SuggestionsQuery().get()
        return context

    def get_queryset_kwargs(self):
        return {'user_id': self.request.user.id}
