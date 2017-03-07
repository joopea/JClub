from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import CreateView, DeleteView, ListView

from apps.core.exceptions import Json404
from apps.core.views import AjaxFormResponseMixin

from apps.community.views import WithCommunity
from lib.behaviours.views import WithAuthor
from apps.menu.views import WithUserMenu

from .queries import FollowUserDataView
from apps.users.queries import FollowingUserDataView, FollowedUserDataView
from .forms import FollowUserForm, FollowCommunityForm
from .models import FollowUser, FollowCommunity


class FollowingListView(WithUserMenu, ListView):
    template_name = 'follow/list.html'
    queryset = FollowUserDataView

    def get_queryset(self):
        return self.queryset.list(author_id=self.request.user.id)


class FollowingUserUsers(object):
    def get_context_data(self, **kwargs):
        context = super(FollowingUserUsers, self).get_context_data(**kwargs)
        users = FollowingUserDataView.list(user=self.request.user)
        context['following'] = users
        context['following_count'] = users.count()
        return context


class FollowedUserUsers(object):
    def get_context_data(self, **kwargs):
        context = super(FollowedUserUsers, self).get_context_data(**kwargs)
        users = FollowedUserDataView.list(user=self.request.user)
        context['followers'] = users
        context['follower_count'] = users.count()
        return context


class AjaxFollowUserCreateView(WithAuthor, AjaxFormResponseMixin, CreateView):

    http_method_names = ['post']

    form_class = FollowUserForm

    def get_extra_data(self):
        context = super(AjaxFollowUserCreateView, self).get_extra_data()
        context['target'] = self.kwargs.get('pk')
        return context


class AjaxFollowUserRemoveView(WithAuthor, AjaxFormResponseMixin, DeleteView):

    http_method_names = ['post']

    model = FollowUser

    def get_extra_data(self):
        context = super(AjaxFollowUserRemoveView, self).get_extra_data()
        context['target'] = self.kwargs.get('pk')
        return context

    def get_object(self, queryset=None):
        args = self.get_extra_data()
        try:
            instance = self.model.objects.get(**args)
        except ObjectDoesNotExist:
            raise Json404()
        return instance


class AjaxFollowCommunityCreateView(WithCommunity, AjaxFollowUserCreateView):
    form_class = FollowCommunityForm


class AjaxFollowCommunityRemoveView(WithCommunity, AjaxFollowUserRemoveView):
    model = FollowCommunity

    def get_extra_data(self):
        context = super(AjaxFollowUserRemoveView, self).get_extra_data()
        context['community'] = self.kwargs.get('pk')
        return context
