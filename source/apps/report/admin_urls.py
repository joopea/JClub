from macrosurl import url
from django.conf.urls import patterns

from .admin import UserReportView
from .admin import ShareReportView
from .admin import FollowersReportView
from .admin import PostReportView
from .admin import LikeReportView
from .admin import CommentReportView
from .admin import AlertsReportView


urlpatterns = patterns(
    '',
    url(r'^user/$', UserReportView.as_view(), name='user_report_view'),
    url(r'^share/$', ShareReportView.as_view(), name='share_report_view'),
    url(r'^like/$', LikeReportView.as_view(), name='like_report_view'),
    url(r'^comment/$', CommentReportView.as_view(), name='comment_report_view'),
    url(r'^post/$', PostReportView.as_view(), name='post_report_view'),
    url(r'^follower/$', FollowersReportView.as_view(), name='follower_report_view'),
    url(r'^alert/$', AlertsReportView.as_view(), name='alert_report_view'),
)

