from django.db import models
from django.utils.translation import ugettext_lazy as _


class ShareAble(models.Model):
    share_count = models.IntegerField(_('Shares'), null=True, default=0)

    class Meta:
        abstract = True
