from .locals import *

INSTANCE_TYPE = 'admin'

ALLOWED_HOSTS = [
    '{{ hostname_admin }}',
]

DEFAULT_FROM_EMAIL = 'no-reply@{{ hostname_admin }}'
SESSION_COOKIE_DOMAIN = '{{ hostname_admin }}'

SECURE_SSL_HOST = '{{ hostname_admin }}'
