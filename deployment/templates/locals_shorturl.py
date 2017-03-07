from .locals import *

ALLOWED_HOSTS = [
    '{{ hostname_shorturl }}',
]

INSTANCE_TYPE = 'shorturl'

INSTALLED_APPS = [
    'apps.shorturl',
]

SECURE_SSL_HOST = '{{ hostname }}'

DEFAULT_FROM_EMAIL = 'no-reply@{{ hostname_shorturl }}'
SESSION_COOKIE_DOMAIN = '{{ hostname_shorturl }}'

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
]
