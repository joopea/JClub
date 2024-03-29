import re
from fabric import colors

from fabric.api import env, sudo
from fabric.context_managers import warn_only, settings
from fabric.contrib.files import exists, upload_template
from fabric.decorators import runs_once
from fabric.operations import prompt
from fabric.utils import abort

from deployscript import utils
from deployscript.services import Service

class Admin(Service):
    env_defaults = {
                    'admin_settings': '{settings_path}locals_admin.py',
                    'admin_template': 'locals_admin.py',
                    }
    
    def deployment(self):
        self.upload_local_settings()

    def upload_local_settings(self):
        utils.var_info('Generating settings', '{admin_settings}'.format(**env))

        if not exists(env.settings_path):
            abort('No settings dir!')

        upload_template(
            'templates/{admin_template}'.format(**env),
            '{admin_settings}'.format(**env),
            context=env, use_jinja=True, template_dir='', use_sudo=True
        )

        sudo('chown {username}:{group} {admin_settings}'.format(**env))

# [program:{{ wsgi_process_name }}]
# command={{ base_path }}releases/current/env/bin/gunicorn -c {{ release_config_path }}gunicorn.conf.py wsgi:application
# directory={{ base_path }}releases/current/source/
# redirect_stderr=true
# user=root

#     def processmanager_conf(self):
#         if env.host not in env.wsgi_hosts:
#             return None
# 
#         return {
#             'environment': {
#                             'DJANGO_SETTINGS_MODULE': 'settings.locals_admin'
#                             },
#             'name': '{wsgi_process_name}_admin',
#             'cmd': '{release_path}/env/bin/gunicorn -c {release_config_path}gunicorn.conf.py wsgi:application',
#             'cwd': '{release_path}source/',
#             'user': 'root',
#         }

