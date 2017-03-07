from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withurl import WithAbsoluteUrl

from lib.behaviours.models.withgenericforeignkey import WithGenericForeignKey
from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor
from lib.behaviours.models.withtarget import WithTarget


class Mention(WithUpdates, WithAuthor, WithTarget, WithAbsoluteUrl, models.Model):
    #user A             WithAuthor
    #   mentions
    #user B             WithTarget
    #   inside a
    #Post or Comment
    #   at a specific
    #DateTime           WithUpdates

    post = models.ForeignKey('post.Post', blank=True, null=True, help_text=_("Choose either a post or comment to report"))
    comment = models.ForeignKey('comment.Comment', blank=True, null=True, help_text=_("Choose either a post or comment to report"))

    def __unicode__(self):
        return _('{0} Mentioned {1}').format(unicode(self.author.name), unicode(self.target.name))

    @property
    def content_object(self):
        """
        Backwards compatible with Generic foreign key
        """
        return self.reported_object

    @content_object.setter
    def content_object(self, value):
        """
        Backwards compatible with Generic foreign key
        """
        if value.__class__.__name__ == 'Post':
            self.post = value

        if value.__class__.__name__ == 'Comment':
            self.comment = value

    @property
    def is_post(self):
        return True if self.post_id else False

    @property
    def is_comment(self):
        return True if self.comment_id else False

    def get_post_id(self):
        if self.is_post:
            return self.post_id
        if self.is_comment:
            return self.comment.post.id

    def save(self, *args, **kwargs):
        if self.comment_id and self.post_id:
            raise Exception("Mention cannot have both post and comment id's")
        super(Mention, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Mention')
        verbose_name_plural = _('Mentions')
        #prevent the same user being mentioned twice in a single comment or post
        #or well, being mentioned twice is ok, but sending twice the message is not
        unique_together = (
            ('author', 'target', 'post'),
            ('author', 'target', 'comment'),
        )
