from django.db import models
from django.utils.translation import ugettext_lazy as _
from lib.behaviours.models.withurl import WithAbsoluteUrl

from lib.behaviours.models.withpost import WithPost
from lib.behaviours.models.withcomment import WithComment


class Approval(models.Model):
    # Todo: Register the part which is matched for approval, so we can show an admin preview

    is_approved = models.BooleanField(_('is approved'), default=False)

    # Todo: Change this to choicefield
    reason = models.TextField(_('reason'), max_length=2048)

    def approve(self):
        raise NotImplemented("Implement this!")

    def disapprove(self):
        raise NotImplemented("Implement this!")

    def get_image(self):
        """
        Returns the image if the approval image is the reason
        """
        raise NotImplemented("Implement this!")

    class Meta:
        abstract = True


class PostApproval(WithPost, Approval, models.Model):

    def __unicode__(self):
        return 'Approval for: %s' % (unicode(self.post), )

    def approve(self):
        self.post.set_published()
        self.post.save()
        self.delete()

    def disapprove(self):
        self.post.delete()
        self.delete()

    def get_image(self):
        if self.reason == 'Image attached':
            return self.post.image

    class Meta:
        verbose_name = _('Post approval')
        verbose_name_plural = _('Post approvals')


class CommentApproval(WithComment, Approval, models.Model):

    def __unicode__(self):
        return 'Approval for: %s' % (unicode(self.comment), )

    def approve(self):
        self.comment.set_published()
        self.comment.save()
        self.delete()

    def disapprove(self):
        self.comment.delete()
        self.delete()

    def get_image(self):
        if self.reason == 'Image attached':
            return self.comment.image

    class Meta:
        verbose_name = _('Comment approval')
        verbose_name_plural = _('Comment approvals')
