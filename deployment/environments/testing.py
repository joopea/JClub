from fabric.api import env

from deployscript.config import Config

env.update(Config(
    is_testing = True,
    hosts = ['IP'],
    hostname = '{project_name}.testing.getlogic.nl',
    network_subnet = '10.0.2.0/24', # Default Tilaa testing cluster

    nginx_use_htpasswd=True,

    django_secret_key = u"KEY",
))
