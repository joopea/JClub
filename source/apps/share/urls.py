from macrosurl import url
from django.conf.urls import patterns

from .views import AjaxCreateShareView


urlpatterns = patterns(
    '',
    url(r'^post/:pk/share/$', AjaxCreateShareView.as_view(), {'model': 'post.Post'}, name='create_ajax'),

)
