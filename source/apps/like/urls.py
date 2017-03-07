from macrosurl import url
from django.conf.urls import patterns

from .views import AjaxLikePostCreateView, AjaxLikePostRemoveView, AjaxLikeCommentCreateView, AjaxLikeCommentRemoveView


urlpatterns = patterns(
    '',
    url(r'^post/:pk/like/$', AjaxLikePostCreateView.as_view(), name='like_post_ajax'),
    url(r'^post/:pk/unlike/$', AjaxLikePostRemoveView.as_view(), name='unlike_post_ajax'),

    url(r'^comment/:pk/like/$', AjaxLikeCommentCreateView.as_view(), name='like_comment_ajax'),
    url(r'^comment/:pk/unlike/$', AjaxLikeCommentRemoveView.as_view(), name='unlike_comment_ajax'),

)
