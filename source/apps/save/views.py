from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, DeleteView, ListView

from apps.core.exceptions import Json404
from apps.core.views import AjaxFormResponseMixin

from lib.behaviours.views import WithAuthor
from apps.menu.views import WithUserMenu

from .forms import SaveForm
from .queries import SaveDataView
from .models import Save


class AjaxSaveCreateView(WithAuthor, AjaxFormResponseMixin, CreateView):

    http_method_names = ['post']

    form_class = SaveForm

    def get_extra_data(self):
        context = super(AjaxSaveCreateView, self).get_extra_data()
        context['post'] = self.kwargs.get('pk')
        return context


class AjaxSaveRemoveView(WithAuthor, AjaxFormResponseMixin, DeleteView):

    http_method_names = ['post']

    model = Save

    def get_object(self, queryset=None):
        args = self.get_extra_data()
        try:
            instance = self.model.objects.get(**args)
        except ObjectDoesNotExist:
            raise Json404()
        return instance

    def get_extra_data(self):
        context = super(AjaxSaveRemoveView, self).get_extra_data()
        context['post'] = self.kwargs.get('pk')
        return context


class SavedListView(WithUserMenu, ListView):
    template_name = 'save/list.html'
    queryset = SaveDataView
    paginate_by = settings.PAGINATION_SIZE

    def get_queryset(self):
        return self.queryset.list(author_id=self.request.user.id)