from .defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

SECRET_KEY = "HXJZZSe.Z5*uWDrJkQ9hBr+UkcAn~8ynr@RW`[JUf,paB7zM/sv&NE}'Qg6SwQD;"
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1']

MONITOR_URL_PATH = '^status\.txt/?$'

INSTANCE_TYPE = 'www'
CHECK_DOMAIN_SEPERATION = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'joopea_development',
        'USER': 'joopea',
        'PASSWORD': 'PzQptGXb8anpm',
        'HOST': 'localhost',
        'PORT': '3306',
        'STORAGE_ENGINE': 'MyISAM',  'InnoDB'
        'OPTIONS': {
            'init_command': 'SET '
                            'storage_engine=InnoDB,'
                            'collation_connection=utf8_bin,'
                            'NAMES utf8,'
                            'character_set_connection=utf8#,'
                            'SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
        }
    }
}

# For profiling
# MIDDLEWARE_CLASSES.insert(0, 'lib.profiling.middleware.ProfileMiddleware')

# ssh -L 3306:127.0.0.1:3306 84.22.97.15

SHORTURL_BASE = "//shorturl.joopea.com:9000/"

AWS_STORAGE_BUCKET_NAME = "joopea-dev"
AWS_ACCESS_KEY_ID = "AKIAJ6FXV43D7Y22CW6A"
AWS_SECRET_ACCESS_KEY = "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"
AWS_AUTO_CREATE_BUCKET = True
AWS_CALLING_FORMAT = OrdinaryCallingFormat
AWS_S3_FILE_OVERWRITE = True
AWS_S3_HOST = "s3.eu-central-1.amazonaws.com"
AWS_S3_CUSTOM_DOMAIN = 'shorturl.joopea.com:9000'

DEBUG_TOOLBAR = True #and False

if DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
    )

    # Debugging toolbar middleware
    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    # JavaScript panels for the deveopment debugging toolbar
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'cachalot.panels.CachalotPanel',
    )
    # Debug toolbar app
    CONFIG_DEFAULTS = {
        'INTERCEPT_REDIRECTS': False,
    }

CACHES = {
    'default': {
        'BACKEND': 'memcached_hashring.backend.MemcachedHashRingCache',
        'LOCATION': ['127.0.0.1']
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '{{ project_code }}: (%(levelname)s:%(name)s) %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False
        },
        ''
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}


# SESSION_EXCLUDED_URLS = [r'^_monitor/$']

# LOGGING['formatters']['verbose']['format'] ='TENA: (%(levelname)s:%(name)s) %(message)s'

SECURE_SSL_REDIRECT = False

