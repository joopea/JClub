from django.contrib.auth import get_user_model
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class WithArchivableAuthor(models.Model):
    author = models.ForeignKey(
        'users.User',
        related_name='author_%(class)s',
        blank=False,
        default=1,
        on_delete=models.SET(get_sentinel_user)
    )

    class Meta:
        abstract = True


class WithAuthor(models.Model):
    author = models.ForeignKey(
        'users.User',
        related_name='author_%(class)s',
        blank=False,
        default=1,
    )

    class Meta:
        abstract = True
