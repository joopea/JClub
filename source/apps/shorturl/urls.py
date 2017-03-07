from apps.shorturl.views import redir

try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

print "Added shorturl urls"
# place app url patterns here
urlpatterns = patterns(
    '',
    url(r'(?P<shorturl>.*)', redir),
)

