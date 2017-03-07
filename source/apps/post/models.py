from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.like.models import LikeAble
from lib.behaviours.models.withurl import WithAbsoluteUrl

from lib.utils.managers import PublishedManager

from lib.behaviours.models.withimage import WithImage
from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.publishable import PublishAble
from lib.behaviours.models.withuser import WithArchivableAuthor
from lib.behaviours.models.commentable import CommentAble
from lib.behaviours.models.saveable import SaveAble
from lib.behaviours.models.shareable import ShareAble
from lib.behaviours.models.withrichtextcontent import WithRichTextContent
from lib.behaviours.models.withcommunity import WithOptionalCommunity


class Post(WithUpdates, WithRichTextContent, PublishAble, WithArchivableAuthor, LikeAble, CommentAble, SaveAble,
           ShareAble, WithAbsoluteUrl, WithImage, WithOptionalCommunity, models.Model):

    title = models.CharField(_('Title'), max_length=160, db_index=True)
    meta = models.CharField(_('Meta'), max_length=72, null=True)

    active = PublishedManager()
    report_builder_model_manager = active
    all_objects = models.Manager()

    needs_approval = False
    dis_approval_reasons = ''

    def __unicode__(self):
        return 'Community: %s - %s' % (unicode(self.community), unicode(self.title[:20]))

    class Meta:
        ordering = ('publish_date', )
        verbose_name = _('Post')
        verbose_name_plural = _("Posts")
