from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import translation
from django.utils.cache import patch_vary_headers
from apps.users.models import User
from django.middleware.locale import LocaleMiddleware

class UserLanguageMiddleware(LocaleMiddleware):

    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        try:
            language = User.objects.get(username=request.user.username).language_id
        except:
            language = settings.LANGUAGE_CODE
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()



