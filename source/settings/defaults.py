import os
from boto.s3.connection import OrdinaryCallingFormat

_ = lambda x: x
PROJECT_DIR = lambda base: os.path.abspath(os.path.join(os.path.dirname(__file__), '../../', base).replace('\\', '/'))

# Django settings
SITE_ID = 1

INSTALLED_APPS = [
    'adminplus',
    'filer',
    'flat',
    'apps.custom_admin',
    'django.contrib.admin',
    'mptt',
    'easy_thumbnails',

    'feincms',
    'adminsortable',

    'apps.cms.pages',
    'apps.core',
    'apps.post',
    'apps.comment',
    'apps.users',
    'apps.like',
    'apps.save',
    'apps.notifications',
    'apps.mention',
    'apps.block',
    'apps.wall',
    'apps.share',
    'apps.community',
    'apps.menu',
    'apps.suggestions',
    'apps.follow',
    'apps.search',
    'apps.report',
    'apps.approval',
    'apps.shorturl',
    'apps.language',

    'lib.cms',
    'lib.utils',

    'django_extensions',
    'djangosecure',
    'widget_tweaks',
    'form_utils',
    'formtools',
    'cachalot',
    'throttle',
    'ckeditor',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'apps.core.middleware.JsonExceptionMiddleware',
    'apps.core.middleware.ForceDefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    # 'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'apps.core.middleware.UserLanguageMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
    'apps.core.middleware.UserRolesDomainSeparation',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

CACHES = {
    'default': {
        'BACKEND': 'memcached_hashring.backend.MemcachedHashRingCache',
        'LOCATION': ['127.0.0.1']
    }
}

# Localization
TIME_ZONE = 'Europe/Amsterdam'
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('fa', _('Persian'))
)

LOCALE_PATHS = [
    PROJECT_DIR('source/locale/')
]

USE_I18N = True
USE_L10N = True
USE_TZ = False

# Root / WSGI
ROOT_URL = ""  # The base url of the website, without trailing slash
ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'wsgi.application'

AUTH_USER_MODEL = 'users.User'
LOGOUT_URL = '/account/logout'
LOGIN_URL = '/'

# Shorturl
SHORTURL_BASE = "//shorturl.joopea.com/"

# Media files
MEDIA_ROOT = PROJECT_DIR('media/')
MEDIA_URL = "/media/"

# Static files
STATIC_ROOT = PROJECT_DIR('static-compiled/')  # Used by django to collect static files 
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
)

# Compressor
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


# Django secure settings
# SECURE_CHECKS
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# no non-TLS url's
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True

# Test settings
# TEST_RUNNER = 'lib.testing_framework.test_runner.ConcreteDiscoverRunner'
TEST_FILES_LOCATION = PROJECT_DIR('') + '/source/lib/testing_framework/media/'
TEST_SELENIUM_DRIVER = PROJECT_DIR('') + '/source/lib/testing_framework/selenium/driver/chromedriver'

# the default pagination size
PAGINATION_SIZE = 20

# DEFAULT_FILE_STORAGE = 'lib.storage.UUIDBotoStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STORAGE_UUID = "6d02732299694f41905a06dea9eda664"

# User Name  GetLogic01
# Access Key Id  AKIAJC5DUUFGDZLQ7YUA
# Secret Access Key  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

AWS_ACCESS_KEY_ID = "AKIAJC5DUUFGDZLQ7YUA"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "joopea-unnamed"
AWS_AUTO_CREATE_BUCKET = False
AWS_CALLING_FORMAT = OrdinaryCallingFormat
AWS_S3_FILE_OVERWRITE = True
AWS_QUERYSTRING_AUTH = False

# BEGIN easy_thumbnail
THUMBNAIL_ALIASES = {
    '': {
        'post_normal': {'size': (250, 250), 'crop': False},
        'community_normal': {'size': (1200, 300), 'crop': False},
        'community_icon_double': {'size': (32, 32), 'crop': False},
        'post_big': {'size': (1000, 750), 'crop': False}
    },
}
# END easy_thumbnail

FILER_IMAGE_TYPES = ['.jpg', '.png', '.jpeg', '.gif']

THROTTLE_ZONES = {
    'admin-login': {
        'VARY': 'apps.core.utils.HashedRemoteIP',
        'NUM_BUCKETS': 2,  # Number of buckets worth of history to keep. Must be at least 2
        'BUCKET_INTERVAL': 60,  # Period of time to enforce limits.
        'BUCKET_CAPACITY': 5,  # Maximum number of requests allowed within BUCKET_INTERVAL
    },
}

# USE FIXED SALT FOR IP THROTTLING CACHE KEYS
THROTTLE_SALT = '-50zLHe*@zevUF5tAY87R|Sg&3=2sYHL'
# USE FIXED ITERATIONS FOR IP THROTTLING CACHE KEYS
THROTTLE_ITERATIONS = 25

# Where to store request counts.
THROTTLE_BACKEND = 'throttle.backends.cache.CacheBackend'

THROTTLE_ENABLED = True


CKEDITOR_UPLOAD_PATH = 'content/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline']
        ],
        'height': 291,
        'width': 400
    }
}

BLEACH_CONFIG = {
    'tags': ['strong', 'b', 'i', 'u', 'em', 'br', 'p'],
    'styles': ['text-decoration']
}

CHECK_DOMAIN_SEPERATION = True

SESSION_COOKIE_AGE = 2*60*60
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
