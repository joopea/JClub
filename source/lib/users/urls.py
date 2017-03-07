from django.conf.urls import patterns, url
from apps.users.views import LoginView, LogoutView
from lib.users.views import PasswordResetView, PasswordResetConfirmView


urlpatterns = patterns(
    '',
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'reset-password/$', PasswordResetView.as_view(), name='password-reset'),
    url(r'reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
)
