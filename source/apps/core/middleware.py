import re

from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.sessions.middleware import SessionMiddleware
from .exceptions import JsonResponseException
from django.http import HttpResponseRedirect
from django.utils import translation
from apps.users.models import User
from django.middleware.locale import LocaleMiddleware




class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers
    
    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies
    
    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            del request.META['HTTP_ACCEPT_LANGUAGE']


class UserLanguageMiddleware(LocaleMiddleware):

    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        try:
            language = User.objects.get(username=request.user.username).language_id
        except:
            language = settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()


class SessionExcludedURLsMiddleware(SessionMiddleware):
    def process_request(self, request):
        if self.is_excluded_url(request):
            request.session = {} # Let's fool AuthMiddleware into thinking session exists
            return

        super(SessionExcludedURLsMiddleware, self).process_request(request)

    def process_response(self, request, response):
        if self.is_excluded_url(request):
            return response

        return super(SessionExcludedURLsMiddleware, self).process_response(request, response)

    def is_excluded_url(self, request):
        if hasattr(request, '_exclude_session'):
            return request._exclude_session

        for pattern in settings.SESSION_EXCLUDED_URLS:
            regex = re.compile(pattern)

            if regex.match(request.path_info):
                request._exclude_session = True
                return True

        request._exclude_session = False

        return False


class JsonExceptionMiddleware(object):

    def process_response(self, request, response):
        if response.status_code == 404 and request.is_ajax():
            return JsonResponse(
                {
                    'success': False,
                    'data': {
                        'status': '404',
                        'message': 'Not found'
                    }
                },
                status=404
            )
        return response

    def process_exception(self, request, exception):
        if request.is_ajax() and isinstance(exception, JsonResponseException):
            kwargs = {}
            response = {
                'success': False,
                'data': {
                    'status': str(getattr(exception, 'status_code', '404')),
                    'message': str(exception)
                }
            }
            return JsonResponse(response, status=404, **kwargs)


class UserRolesDomainSeparation(object):
    def process_request(self, request):
        if settings.CHECK_DOMAIN_SEPERATION:
            if request.user.is_authenticated():
                if settings.INSTANCE_TYPE == 'www' and request.user.is_staff:
                    raise PermissionDenied
                if settings.INSTANCE_TYPE == 'admin' and not request.user.is_staff:
                    raise PermissionDenied
