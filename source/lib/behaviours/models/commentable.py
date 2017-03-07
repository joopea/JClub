from django.db import models
from django.utils.translation import ugettext_lazy as _


class CommentAble(models.Model):
    comment_count = models.IntegerField(_('Comments'), null=True, default=0)

    class Meta:
        abstract = True

