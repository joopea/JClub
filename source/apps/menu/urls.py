from macrosurl import url
from django.conf.urls import patterns

from .views import AjaxCommunitiesPanel, AjaxFollowingPanel, AjaxNotificationsPanel, AjaxNotificationsCount


urlpatterns = patterns(
    '',
    url(r'^communities$', AjaxCommunitiesPanel.as_view(), name='communities_ajax'),
    url(r'^following', AjaxFollowingPanel.as_view(), name='following_ajax'),
    url(r'^notifications/count', AjaxNotificationsCount.as_view(), name='notifications_count_ajax'),
    url(r'^notifications', AjaxNotificationsPanel.as_view(), name='notifications_ajax'),
)
