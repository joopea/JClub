from django.conf.urls import patterns, url
from apps.users.views import LoginView, LogoutView, RegisterView, UserDetailsView, UsernameVariationView, \
    PasswordResetView, ProfileDeleteView

urlpatterns = patterns(
    '',
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'register/$', RegisterView.as_view(), name='register_ajax'),
    url(r'user-details/$', UserDetailsView.as_view(), name='user-details'),
    url(r'username-variants/$', UsernameVariationView.as_view(), name='user-variants'),
    url(r'reset-password/$', PasswordResetView.as_view(), name='password-reset'),
    url(r'delete/$', ProfileDeleteView.as_view(), name='delete'),
)
