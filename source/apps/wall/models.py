from django.db import models
from lib.behaviours.models.withcommunity import WithCommunity
from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor
from lib.behaviours.models.withurl import WithAbsoluteUrl
from django.utils.translation import ugettext_lazy as _


class Wall(WithAbsoluteUrl, WithAuthor, WithUpdates, models.Model):
    post = models.ForeignKey('post.Post', related_name='wall_posts')
    is_read = models.BooleanField(default=False)

    def __unicode__(self):
        return u'wall of %s' % (unicode(self.author), )

    class Meta:
        ordering = ('created', )
        verbose_name = _('Wall')
        verbose_name_plural = _("Wall")
        unique_together = (("author", "post"),)
        index_together = (("author", "post"),)


class CommunityWall(WithAbsoluteUrl, WithCommunity, WithUpdates, models.Model):
    post = models.ForeignKey('post.Post', related_name='community_wall_posts')

    def __unicode__(self):
        return u'community wall of %s' % (unicode(self.community), )

    class Meta:
        ordering = ('created', )
        verbose_name = _('Community Wall')
        verbose_name_plural = _("Community Walls")
