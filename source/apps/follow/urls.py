from macrosurl import url

from django.conf.urls import patterns

from .views import FollowingListView, AjaxFollowUserCreateView, AjaxFollowUserRemoveView, \
    AjaxFollowCommunityCreateView, AjaxFollowCommunityRemoveView


urlpatterns = patterns(
    '',

    url(r'^user/follow/user/:pk/$', AjaxFollowUserCreateView.as_view(), name='follow_user_ajax'),
    url(r'^user/unfollow/user/:pk/$', AjaxFollowUserRemoveView.as_view(), name='unfollow_user_ajax'),

    url(r'^user/follow/community/:pk/$', AjaxFollowCommunityCreateView.as_view(), name='follow_community_ajax'),
    url(r'^user/unfollow/community/:pk/$', AjaxFollowCommunityRemoveView.as_view(), name='unfollow_community_ajax'),

    url(r'^user/following/$', FollowingListView.as_view(), name='list'),

)
