from django.db import models
from django.utils.translation import ugettext_lazy as _


class Language(models.Model):
    ACTIVE = True
    DEACTIVATED = False
    LANGUAGE_STATUS = (
        (ACTIVE, 'Active'),
        (DEACTIVATED, 'Deactivated'),
    )
    name = models.CharField(max_length=15)
    initial = models.CharField(max_length=3)
    status = models.BooleanField(
        # max_length=5,
        choices=LANGUAGE_STATUS,
        default=DEACTIVATED
    )

    # def __unicode__(self):
    #     return unicode(self.status)