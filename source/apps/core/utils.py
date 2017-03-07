import binascii
from django.conf import settings
from django.utils.crypto import pbkdf2
from django.utils.translation import ugettext_lazy as _
import hashlib
from throttle.zones.remoteip import RemoteIP

class FileBrowserImageSize(object):
    """
    Filebrowser Image size. Perhaps needs to be combined with the filebrowser settings for consistency.

    For now see: settings.FILEBROWSER_VERSIONS (keys match constants)
    """

    #Todo: Just a stub, you need to implement this for your site
    ONE_COL = 'one'
    TWO_COL = 'two'
    THREE_COL = 'three'

    PAGE_LARGE = 'page_large'
    PAGE_SMALL = 'page_small'

    SIZES = (
        (ONE_COL, 'Een kolom'),
        (TWO_COL, 'Twee kolommen'),
        (THREE_COL, 'Drie kolommen')
    )

    @classmethod
    def default(cls):
        return cls.ONE_COL


class HashedRemoteIP(RemoteIP, object):
    """ Custom bucket key generator for django-throttle-requests, IP addresses
        are hashed with django.utils.crypt.pbkdf2
    """
    def get_bucket_key(self, *args, **kwargs):
        ip_address = super(HashedRemoteIP, self).get_bucket_key(*args, **kwargs)

        bucket_key = pbkdf2(
            ip_address,
            self.get_salt(),
            self.get_iterations(),
            digest=hashlib.sha256
        )

        bucket_key = binascii.b2a_hex(bucket_key)

        return bucket_key

    def get_salt(self):
        # USE FIXED SALT
        return settings.THROTTLE_SALT

    def get_iterations(self):
        # USE FIXED NUMBER OF ITERATIONS
        return settings.THROTTLE_ITERATIONS

