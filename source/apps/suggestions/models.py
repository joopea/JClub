from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withurl import WithAbsoluteUrl

from lib.behaviours.models.withupdates import WithUpdates


class HottestPost(WithUpdates, WithAbsoluteUrl, models.Model):
    post = models.ForeignKey('post.Post')

    interval = models.IntegerField(_('Interval in days'), default=0)

    like_ratio = models.DecimalField(_('Multiplier for like-count'), decimal_places=2, max_digits=5, default=0)
    share_ratio = models.DecimalField(_('Multiplier for share-count'), decimal_places=2, max_digits=5, default=0)
    comment_ratio = models.DecimalField(_('Multiplier for comment-count'), decimal_places=2, max_digits=5, default=0)

    def __unicode__(self):
        return '%s' % (unicode(self.post.title[0:128]), )

    class Meta:
        ordering = ('modified', )
        verbose_name = _('Hottest Post')


class PromotedPost(WithUpdates, WithAbsoluteUrl, models.Model):
    post = models.ForeignKey('post.Post')

    def __unicode__(self):
        return '%s' % (unicode(self.post.title[0:128]), )

    class Meta:
        ordering = ('modified', )
        verbose_name = _('Promoted Post')


class HottestCommunity(WithUpdates, WithAbsoluteUrl, models.Model):
    community = models.ForeignKey('community.Community')

    interval = models.IntegerField(_('Interval in days'), default=0)

    like_ratio = models.DecimalField(_('Multiplier for like-count'), decimal_places=2, max_digits=5, default=0)
    share_ratio = models.DecimalField(_('Multiplier for share-count'), decimal_places=2, max_digits=5, default=0)
    comment_ratio = models.DecimalField(_('Multiplier for comment-count'), decimal_places=2, max_digits=5, default=0)
    post_ratio = models.DecimalField(_('Multiplier for post-count'), decimal_places=2, max_digits=5, default=0)

    def __unicode__(self):
        return '%s' % (unicode(self.community), )

    class Meta:
        ordering = ('modified', )
        verbose_name = _('Hottest Community')
        verbose_name_plural = _('Hottest Communities')
