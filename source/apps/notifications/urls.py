from macrosurl import url

from django.conf.urls import patterns

from .views import NotificationList, AjaxMarkNotificationAsRead


urlpatterns = patterns(
    '',
    url(r'^notifications/$', NotificationList.as_view(), name='list'),
    url(r'^notification/:pk/is_read', AjaxMarkNotificationAsRead.as_view(), name='is_read')

)
