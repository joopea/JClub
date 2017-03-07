from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withurl import WithAbsoluteUrl

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor
from lib.behaviours.models.withcommunity import WithCommunity


class FollowCommunity(WithUpdates, WithAuthor, WithCommunity, WithAbsoluteUrl, models.Model):
    def __unicode__(self):
        return 'follower: {0}\ncommunity: {1}'.format(unicode(self.author), unicode(self.community))

    class Meta:
        verbose_name = _('Follow community')
        verbose_name_plural = _('Follow communities')
        unique_together = (('author', 'community'), )


class FollowUser(WithUpdates, WithAuthor, WithAbsoluteUrl, models.Model):
    def __unicode__(self):
        return 'follower: {0}\nfollowee: {1}'.format(unicode(self.author), unicode(self.target))

    target = models.ForeignKey('users.User', related_name='followed_user')

    class Meta:
        verbose_name = _('Follow user')
        verbose_name_plural = _('Follow users')
        unique_together = (('author', 'target'))
