from fabric.api import env

from deployscript.config import Config

env.update(Config(
    debug = True,
    is_staging = True,
    hostname = '{project_name}.staging.getlogic.nl',
    network_subnet = '10.0.0.0/24',  # Default Tilaa staging cluster

    nginx_use_htpasswd = False,

    hosts = ['IP'],
    wsgi_hosts = ['IP'],
    hostname_media = 'media.{project_name}.staging.getlogic.nl',
    hostname_shorturl = 'redir.{project_name}.staging.getlogic.nl',

    db_engine = 'django.db.backends.postgresql_psycopg2',

    django_secret_key = """KEY""",

))
