import os

from fabric.api import env

from deployscript.config import Config

env.update(Config(
    is_development = True,
    debug = True,
    hosts = ['IP'],
    wsgi_hosts = ['IP'],
    hostname = '{project_name}.jassist.eu',
    network_subnet = '10.0.2.0/24', # Default Tilaa testing cluster

    db_engine = 'django.db.backends.mysql',
    db_password = 'PASSWD',
    db_storage_engine = 'MyISAM',
    db_options = {
        'init_command': 'SET '
                'storage_engine=MyISAM,'
                'collation_connection=utf8_bin,'
                'NAMES utf8,'
                'character_set_connection=utf8,'
                'SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED',
    },

    nginx_use_htpasswd=True,

    django_secret_key = u"SECRET KEY",
))
