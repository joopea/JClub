from macrosurl import url
from django.conf.urls import patterns

from apps.search import views


urlpatterns = patterns(
    '',
    url(r'^$', views.SearchView.as_view(), name='search'),
)
