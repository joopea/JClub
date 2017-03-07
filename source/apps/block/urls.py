from macrosurl import url
from django.conf.urls import patterns
from apps.block.views import AjaxBlockUserView, AjaxUnBlockUserView

urlpatterns = patterns(
    '',

    url(r'^user/block/user/:pk/$', AjaxBlockUserView.as_view(), name='block_user_ajax'),
    url(r'^user/unblock/user/:pk/$', AjaxUnBlockUserView.as_view(), name='unblock_user_ajax'),
)

