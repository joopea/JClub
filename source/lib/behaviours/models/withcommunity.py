from django.db import models


class WithCommunity(models.Model):
    community = models.ForeignKey('community.Community', related_name='community_%(class)s', blank=False, default=1)

    class Meta:
        abstract = True


class WithOptionalCommunity(models.Model):
    community = models.ForeignKey('community.Community', related_name='community_%(class)s', blank=True, null=True,
                                  default=None)

    class Meta:
        abstract = True
