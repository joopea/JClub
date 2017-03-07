from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, DeleteView
from apps.block.forms import BlockUserForm
from apps.block.models import BlockByUser
from apps.core.exceptions import Json404
from apps.core.views import AjaxFormResponseMixin
from lib.behaviours.views import WithAuthor
from .queries import BlockedUsersDataView


class BlockedUsers(object):
    def get_context_data(self, **kwargs):
        context = super(BlockedUsers, self).get_context_data(**kwargs)
        blocked = BlockedUsersDataView.list(user=self.request.user)
        context['blocked'] = blocked
        context['blocked_count'] = blocked.count()
        return context


class AjaxBlockUserView(WithAuthor, AjaxFormResponseMixin, CreateView):
    http_method_names = ['post']
    form_class = BlockUserForm

    def get_extra_data(self):
        context = super(AjaxBlockUserView, self).get_extra_data()
        context['target'] = self.kwargs.get('pk')
        return context


class AjaxUnBlockUserView(WithAuthor, AjaxFormResponseMixin, DeleteView):
    http_method_names = ['post']
    model = BlockByUser

    def get_extra_data(self):
        context = super(AjaxUnBlockUserView, self).get_extra_data()
        context['target'] = self.kwargs.get('pk')
        return context

    def get_object(self, queryset=None):
        args = self.get_extra_data()
        try:
            instance = self.model.objects.get(**args)
        except ObjectDoesNotExist:
            raise Json404()
        return instance
