from django.db import models


class WithTarget(models.Model):
    target = models.ForeignKey('users.User', related_name='target_%(class)s', blank=False, default=1)

    class Meta:
        abstract = True
