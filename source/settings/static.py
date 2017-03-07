from .defaults import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

SECRET_KEY = "HXJZZSe.Z5*uWDrJkQ9hBr+UkcAn~8ynr@RW`[JUf,paB7zM/sv&NE}'Qg6SwQD;"
ALLOWED_HOSTS = ['*']

MONITOR_URL_PATH = '^status\.txt/?$'

#@TODO Digital Road: https://docs.djangoproject.com/en/dev/ref/databases/#mysql-collation, set collation to utf8_bin
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'joopea_development',
        'USER': 'joopea_dev',
        'PASSWORD': 'YUWYHvLKT3cnADVm',
        'HOST': 'localhost',
        'PORT': '3306',
        'STORAGE_ENGINE': 'MyISAM',
        'OPTIONS': {
            'init_command': 'SET storage_engine=MyISAM,character_set_connection=utf8_bin,collation_connection=utf8_bin',
        }
    }
}


# SESSION_EXCLUDED_URLS = [r'^_monitor/$']

# LOGGING['formatters']['verbose']['format'] ='TENA: (%(levelname)s:%(name)s) %(message)s'
