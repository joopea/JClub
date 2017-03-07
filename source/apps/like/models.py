from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor
from lib.behaviours.models.withgenericforeignkey import WithGenericForeignKey


class Like(WithUpdates, WithAuthor, models.Model):
    class Meta:
        abstract = True


class LikePost(Like):
    post = models.ForeignKey('post.Post', related_name='post_like')

    def __unicode__(self):
        return '%s likes %s' % (unicode(self.author.get_username()), unicode(self.post.title))

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _("Likes")
        unique_together = (
            ('author', 'post'),
        )


class LikeComment(Like):
    comment = models.ForeignKey('comment.Comment')

    def __unicode__(self):
        return '%s likes %s' % (unicode(self.author.get_username()), unicode(self.comment))

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _("Likes")
        unique_together = (
            ('author', 'comment'),
        )


class LikeAble(models.Model):
    like_count = models.IntegerField(_('Likes'), null=True, default=0)

    class Meta:
        abstract = True
