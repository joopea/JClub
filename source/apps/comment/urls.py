from macrosurl import url

from django.conf.urls import patterns, include

from .views import CommentCreate, CommentList, CommentDelete, FirstAndLastComments


urlpatterns = patterns(
    '',

    url(r'^post/:pk/comment/create/$', CommentCreate.as_view(), name='create'),
    url(r'^post/:pk/comments/more/$', CommentList.as_view(), name='more'),
    url(r'^post/:pk/comments/first_last/$', FirstAndLastComments.as_view(), name='first_and_last'),

    url(r':pk/delete/$', CommentDelete.as_view(), name='delete_ajax'),
    url(r':pk/', include('apps.report.urls', namespace='report'), {'model': 'comment.Comment'}),

)
