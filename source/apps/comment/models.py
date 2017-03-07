from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withurl import WithAbsoluteUrl
from apps.like.models import LikeAble

from lib.utils.managers import PublishedManager

from lib.behaviours.models.withimage import WithImage
from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.publishable import PublishAble
from lib.behaviours.models.withuser import WithArchivableAuthor
from lib.behaviours.models.withrichtextcontent import WithRichTextContent


class Comment(WithUpdates, LikeAble, WithImage, WithRichTextContent, PublishAble, WithArchivableAuthor, WithAbsoluteUrl, models.Model):
    post = models.ForeignKey('post.Post')

    # Todo: Why assign to active? Shouldn't this be the ActiveManager?
    # Todo: Published comments are not implemented?? Date is never set ...
    active = PublishedManager()
    all_objects = models.Manager()

    needs_approval = False
    dis_approval_reasons = ''

    def __unicode__(self):
        return unicode(self.message[0:128])

    class Meta:
        ordering = ('created', )
        verbose_name = _('Comment')
        verbose_name_plural = _("Comments")
