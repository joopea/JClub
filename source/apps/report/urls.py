from macrosurl import url
from django.conf.urls import patterns

from .views import AjaxCreatePostReportView, AjaxCreateCommentReportView


urlpatterns = patterns(
    '',
    url(r'^post/:pk/report/$', AjaxCreatePostReportView.as_view(), name='post_create_ajax'),
    url(r'^comment/:pk/report/$', AjaxCreateCommentReportView.as_view(), name='comment_create_ajax'),
)
