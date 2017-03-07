from fabric.api import env

from deployscript.config import Config

env.update(Config(
    is_development = False,
    is_testing = False,
    is_staging = False,
    is_live = False,
    hostname_media = "media.{hostname}",
    hostname_shorturl = "redir.{hostname}",
    hostname_admin = "admin.{hostname}",

    aws_storage_bucket_name="joopea-dev",
    aws_access_key_id="ID",
    aws_secret_access_key="KEY",
    aws_s3_host="s3.eu-central-1.amazonaws.com",
    aws_s3_custom_domain="jimg.eu",
    aws_auto_create_bucket=False,
    aws_s3_file_overwrite=True,
    aws_querystring_auth=False,

))
