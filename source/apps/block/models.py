from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor
from lib.behaviours.models.withtarget import WithTarget
from lib.behaviours.models.withcommunity import WithCommunity


class BlockByUser(WithUpdates, WithAuthor, WithTarget, models.Model):
    def __unicode__(self):
        return 'blockee: {0} blocker: {1}'.format(unicode(self.target.username), unicode(self.author.username))

    class Meta:
        verbose_name = _('Block by user')
        verbose_name_plural = _('Blocked by users')
        unique_together = (('author', 'target'),)


class BlockByCommunity(WithUpdates, WithTarget, WithCommunity, models.Model):
    def __unicode__(self):
        return 'blockee: {0} community: {1}'.format(unicode(self.target.username), unicode(self.community.name))

    class Meta:
        verbose_name = _('Block by community')
        verbose_name_plural = _('Blocked by communities')
        unique_together = (('target', 'community'),)
