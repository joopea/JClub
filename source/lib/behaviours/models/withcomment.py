from django.core.urlresolvers import reverse
from django.db import models


class WithComment(models.Model):
    comment = models.ForeignKey('comment.Comment', related_name='comment_%(class)s', blank=False, default=0)

    class Meta:
        abstract = True
