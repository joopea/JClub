from django.db import models
from django.utils.translation import ugettext_lazy as _
from lib.utils.managers import ActiveManager

'''Here is simple model with choice'''


class Language(models.Model):
    ACTIVE = 'act'
    DEACTIVATED = 'deact'
    LANGUAGE_STATUS = (
        (ACTIVE, 'Active'),
        (DEACTIVATED, 'Deactivated'),
    )
    name = models.CharField(_('name'), max_length=15, unique=True)
    initial = models.CharField(max_length=3, primary_key=True)
    status = models.CharField(
        max_length=5,
        choices=LANGUAGE_STATUS,
        default=DEACTIVATED
    )

    def __unicode__(self):
        return unicode(self.name)

'''Here is model like model in users names'''


# class Language(models.Model):
#     name = models.CharField(_('name'), max_length=15, unique=True)
#     initial = models.CharField(max_length=3)
#     status = models.BooleanField(_('active'), default=False)
#
#     objects = ActiveManager()
#
#     def change(self, **kwargs):
#         self.status = True
#         self.save()
#
#     def __unicode__(self):
#         return unicode(self.name)

