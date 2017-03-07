from django.db import models
from django.conf import settings
import uuid


class ShortURLManager(models.Manager):
    def active(self):
        return super(ShortURLManager, self).get_queryset().filter(active=True)


class ShortURL(models.Model):
    short = models.UUIDField(primary_key=True, default=uuid.uuid4)
    long = models.URLField(unique=True, max_length=255)
    ttl = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    objects = ShortURLManager()

    @property
    def url(self):
        # Donot forget to end the SHORTURL_BASE with a slash
        if self.short is None:
            # Flush to get generated values
            self.save()
        base = settings.SHORTURL_BASE
        if callable(base):
            base = base()
        return base + unicode(self.short)

    def __str__(self):
        return self.url

    def __repr__(self):
        return unicode(self.short)+unicode((self.long, self.ttl))