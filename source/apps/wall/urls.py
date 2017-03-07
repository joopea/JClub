from macrosurl import url

from django.conf.urls import patterns
from apps.wall.views import WallList, CommunityWallList, AjaxMarkWallPostAsRead, WallOwnPostsList

urlpatterns = patterns(
    '',

    url(r'^user/', WallList.as_view(), name='user'),
    url(r'^user/own/', WallOwnPostsList.as_view(), name='own'),
    url(r'^user/:pk/', WallList.as_view(), name='detail'),

    url(r'^community/:pk/', CommunityWallList.as_view(), name='community'),

    url(r'^post/:pk/is_read', AjaxMarkWallPostAsRead.as_view(), name='is_read')

)

