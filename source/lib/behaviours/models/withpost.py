from django.core.urlresolvers import reverse
from django.db import models


class WithPost(models.Model):
    post = models.ForeignKey('post.Post', related_name='post_%(class)s', blank=False, default=1)

    class Meta:
        abstract = True
