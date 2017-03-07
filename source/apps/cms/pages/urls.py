from django.conf.urls import patterns, url
from apps.cms.pages import views


urlpatterns = patterns(
    'apps.cms.pages.views',

    url(r'^(?P<slug>[-\w]+)/$', views.PageDetailView.as_view(), name='detail'),
)
