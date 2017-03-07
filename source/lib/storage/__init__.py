import uuid
import os

from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

STORAGE_UUID = uuid.UUID(settings.STORAGE_UUID)  # Parse uuid from settings
        
    
class UUIDBotoStorage(S3BotoStorage):
    def get_available_name(self, name):
        """ Overwrite existing file with the same name. """
        path, filename = os.path.split(name)
        filename = filename.encode('ascii')
        new_name = uuid.uuid5(STORAGE_UUID, filename).hex
#         new_name = uuid.uuid4().hex
        name_parts = name.rsplit('.', 1)  # Gives mostly 2 results
        if len(name_parts) == 2:  # The file name has an extension
            new_name = '.'.join((new_name, name_parts[1]))
        return os.path.join(path, new_name)
