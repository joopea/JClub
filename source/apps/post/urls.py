from macrosurl import url

from django.conf.urls import patterns, include

from .views import PostDetail, PostDelete, PostCreate


urlpatterns = patterns(
    '',
    url(r'create/$', PostCreate.as_view(), name='create_ajax', kwargs={'model': 'post.Post'}),

    url(r':pk/$', PostDetail.as_view(), name='detail'),
    url(r':pk/delete/$', PostDelete.as_view(), name='delete_ajax'),

    url(r':pk/', include('apps.share.urls', namespace='share'), {'model': 'post.Post'}),

)
