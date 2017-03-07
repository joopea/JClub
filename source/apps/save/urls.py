from macrosurl import url
from django.conf.urls import patterns

from .views import AjaxSaveCreateView, AjaxSaveRemoveView, SavedListView


urlpatterns = patterns(
    '',
    url(r'^save/$', SavedListView.as_view(), name='list'),

    url(r'^post/:pk/save/$', AjaxSaveCreateView.as_view(), {'model': 'post.Post'}, name='save_ajax'),
    url(r'^post/:pk/unsave/$', AjaxSaveRemoveView.as_view(), {'model': 'post.Post'}, name='unsave_ajax'),
)

