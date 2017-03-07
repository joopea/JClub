from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, View
from django.http import HttpResponseForbidden, JsonResponse
from apps.users.forms import LoginForm
from apps.users.queries import UserProfile

from apps.community.queries import MenuUserCommunityDataView
from apps.follow.queries import MenuUserFollowUserDataView
from apps.notifications.queries import NotificationDataView


class WithUserMenu(object):
    def get_context_data(self, *args, **kwargs):
        context = super(WithUserMenu, self).get_context_data(*args, **kwargs)
        context['profile'] = UserProfile.get(self.request.user.pk)
        if not self.request.user.is_authenticated():
            context['login_form'] = LoginForm(prefix='user')
            context['login_form_action'] = reverse_lazy("users:login")
        return context


class AjaxCommunitiesPanel(TemplateView):
    template_name = 'menu/ajax/_communities.html'

    def get_context_data(self, **kwargs):
        context = super(AjaxCommunitiesPanel, self).get_context_data(**kwargs)
        context['communities'] = list(MenuUserCommunityDataView.list(user_id=self.request.user.id))
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(AjaxCommunitiesPanel, self).get(self, *args, **kwargs)


class AjaxFollowingPanel(TemplateView):
    template_name = 'menu/ajax/_following.html'

    def get_context_data(self, **kwargs):
        context = super(AjaxFollowingPanel, self).get_context_data(**kwargs)
        context['following'] = list(MenuUserFollowUserDataView.list(user_id=self.request.user.id))
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(AjaxFollowingPanel, self).get(self, *args, **kwargs)


class AjaxNotificationsPanel(TemplateView):
    template_name = 'menu/ajax/_notifications.html'

    def get_context_data(self, **kwargs):
        context = super(AjaxNotificationsPanel, self).get_context_data(**kwargs)
        context['notifications'] = NotificationDataView.by_user(user_id=self.request.user.id)
        return context

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(AjaxNotificationsPanel, self).get(self, *args, **kwargs)


class AjaxNotificationsCount(View):
    http_method_names = ['get']

    def get(self, *args, **kwargs):
        return JsonResponse(
            NotificationDataView.get_unread_notifications_count(user_id=self.request.user.id),
            safe=False
        )


