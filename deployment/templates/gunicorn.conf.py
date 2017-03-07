user = '{{ username }}'
group = '{{ username }}'
bind = 'unix://{{ wsgi_socket }}'
pidfile = '{{ wsgi_pid }}'
errorlog = '{{ wsgi_log }}'
loglevel = 'warning'

workers = '{{ wsgi_workers }}'
deamon = True
max_requests = {{ wsgi_max_requests }}

#worker_class = 'sync'
preload_app = False
