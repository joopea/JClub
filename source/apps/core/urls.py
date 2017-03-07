from django.conf.urls import url, patterns, include
from django.views.generic import TemplateView

from django.conf import settings

urlpatterns = patterns(
    '',
    url(settings.MONITOR_URL_PATH, TemplateView.as_view(template_name='core/status.txt')),
    url(r'^robots\.txt/?$', TemplateView.as_view(template_name='core/robots.txt')),

)
