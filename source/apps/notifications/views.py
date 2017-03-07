from django.conf import settings
from django.http import JsonResponse
from django.views.generic import ListView, CreateView

from apps.menu.views import WithUserMenu

from .queries import NotificationDataView


class NotificationList(WithUserMenu, ListView):
    template_name = 'notifications/list.html'
    queryset = NotificationDataView
    paginate_by = settings.PAGINATION_SIZE

    def get_queryset(self):
        return self.queryset.list(owner_id=self.request.user.id)


class AjaxMarkNotificationAsRead(CreateView):
    http_method_names = ['post']

    def get_object(self, queryset=None):
        return NotificationDataView.get(id=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        object = self.get_object()
        object.read = True
        object.save()
        return JsonResponse({'success': True})
