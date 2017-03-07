from django.db import models
from django.utils.translation import ugettext_lazy as _
from lib.behaviours.models.withgenericforeignkey import WithGenericForeignKey

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor


class Report(WithUpdates, WithAuthor, models.Model):
    post = models.ForeignKey('post.Post', blank=True, null=True, on_delete=models.CASCADE, help_text=_("Choose either a post or comment to report"))
    comment = models.ForeignKey('comment.Comment', blank=True, null=True, on_delete=models.CASCADE, help_text=_("Choose either a post or comment to report"))
    message = models.TextField(_('Message'), max_length=8192, help_text=_("This message will be sent to the user, if this report is approved"))

    def __unicode__(self):
        return '%s reported message: %s' % (unicode(self.author.username), unicode(self.message[0:128]))

    def approve(self):
        self.reported_object.delete()
        self.delete()

    def disapprove(self):
        self.delete()

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
    def reported_object(self):
        return self.comment or self.post

    def get_absolute_url(self):
        return self.reported_object.get_absolute_url()

    @property
    def is_post(self):
        return True if self.post_id else False

    @property
    def is_comment(self):
        return True if self.comment_id else False

    @property
    def reported_user(self):
        return self.reported_object.author

    def get_post_id(self):
        if self.is_post:
            return self.post_id
        if self.is_comment:
            return self.comment.post.id

    def save(self, *args, **kwargs):
        if self.comment_id and self.post_id:
            raise Exception("Report cannot have both post and comment id's")
        if not self.comment_id and not self.post_id:
            raise Exception("Report must have post or comment id")
        super(Report, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created', )
        verbose_name = _('Report')
        verbose_name_plural = _("Reports")
