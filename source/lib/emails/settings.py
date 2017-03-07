from django.conf import settings

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', '')
CUSTOMER_EMAIL = getattr(settings, 'CUSTOMER_EMAIL', '')
