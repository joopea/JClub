from macrosurl import url

from django.conf.urls import patterns

from .views import CommunityListView


urlpatterns = patterns(
    '',
    url(r'^community/$', CommunityListView.as_view(), name='list'),
)
