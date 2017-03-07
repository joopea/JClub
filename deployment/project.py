from collections import OrderedDict

from fabric.api import env

from services.shorturl import ShortUrl
from services.admin import Admin
from services.gunicorn_shorturl import GunicornShortUrl
from services.gunicorn_admin import GunicornAdmin
from deployscript import services, utils
from deployscript.config import Config

from environments import _common

# Set this to True to enable a whole bunch of debugging messages during deployment
env.debug = False

env.update(Config(
    project_name = 'joopea',

    # Short uppercase project code, should be identical to internal tools
    project_code = 'joopea',

    hosts = ['127.0.0.1'],
    username = 'joopea',
    group = 'joopea',

    hostname = 'Not Used',
    db_engine = 'django.db.backends.postgresql_psycopg2',
    db_host = 'localhost',
    db_password = '',
    db_user='{project_name}',
    db_name='{project_env}',

    django_secret_key = 'Not Used',

    nginx_allowed_ips = { # IP ranges exempt from basic authentication (testing/staging)
        'IP': 'Name',
    },
))

env.deploy_steps = [
    'select_environment',
    'select_revision',
    'set_environment',
    'check_environment',
    'bootstrap',
    'identify',
    'deployment_init',
    'deployment',
    'generate_config',
    'maintenance_init',
    'maintenance',
    'maintenance_finish',
    'in_maintenance',
    'unmaintenance_init',
    'unmaintenance',
    'unmaintenance_finish',
    'deployment_finish',
]

env.services = OrderedDict([
#     ('acks', services.Acks()),
    ('otap', services.OTAP()),
    ('codebase', services.Mercurial()),
    ('virtualenv', services.Virtualenv()),
    ('shorturl', ShortUrl()),
    ('admin', Admin()),
    ('cache', services.Redis()),
#     ('database', services.PostgreSQL()),
    ('wgsi', services.Gunicorn()),
    ('wsgi_shorturl', GunicornShortUrl()),
    ('wsgi_admin', GunicornAdmin()),
    ('async_queue', services.Celery()),
    ('http_cache', services.Varnish()),
    ('project', services.Django()),
    ('webserver', services.Nginx()),
#     ('loadbalancer', services.NginxLoadbalancer()),
    ('process_manager', services.Supervisor()),
])

env.environments = ['development', 'testing', 'staging', 'live']
