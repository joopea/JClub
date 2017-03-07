from macrosurl import url
from django.conf.urls import patterns

from .views import SuggestionListView


urlpatterns = patterns(
    '',
    url(r'^suggestions/$', SuggestionListView.as_view(), name='list'),
)

