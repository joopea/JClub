from django.conf import settings

# These you probably want to change
LOGIN_URL = getattr(settings, 'LOGIN_URL', '/')
LOGOUT_URL = getattr(settings, 'LOGOUT_URL', '/')
LANGUAGE_CODE = getattr(settings, 'LANGUAGE_CODE', 'fa')
