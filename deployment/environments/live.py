from fabric.api import env

from deployscript.config import Config

env.update(Config(
    is_live=True,
    email_use_whitelist='False',
    network_subnet='10.0.5.0/24',  # Default Tilaa shared live cluster
    hosts=['IP'],    # '37.252.127.97'],
    wsgi_hosts=['IP'],   # '37.252.127.97'],
    hostname='jclub.jassist.eu',
    hostname_media="jimg.jassist.eu",
    hostname_admin='j-ad.jassist.eu',
    hostname_shorturl='redir.jimg.jassist.eu',
    memcached_hosts=['10.0.5.109'],
    db_engine='django.db.backends.postgresql_psycopg2',
    django_secret_key=u"KEY",
    aws_access_key_id="ID",
    aws_storage_bucket_name="joopea-live",
    aws_auto_create_bucket=False,
    aws_s3_file_overwrite=True,
    aws_querystring_auth=False,
    aws_s3_host="s3-website-eu-west-1.amazonaws.com"#s3.eu-central-1.amazonaws.com"
    # aws_storage_bucket_name="joopea-live",
    # aws_access_key_id="ID",
    # aws_secret_access_key="KEY",
    # aws_s3_host="s3-website-eu-west-1.amazonaws.com"
))


#     roledefs = {
#                 'wsgi': {
#                     'hosts': ['84.22.99.55', '37.252.127.97']
#                     }
#                 },
