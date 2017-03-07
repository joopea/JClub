from django.db import models
from django.utils.translation import ugettext_lazy as _


class SaveAble(models.Model):
    save_count = models.IntegerField(_('Saves'), null=True, default=0)

    class Meta:
        abstract = True
