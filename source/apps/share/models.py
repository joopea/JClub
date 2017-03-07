from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor
from lib.behaviours.models.withpost import WithPost


class Share(WithUpdates, WithAuthor, WithPost, models.Model):
    """ This model is NOT USED: Find shares by filtering post.wall_post
    """

    def __unicode__(self):
        return _('{0} shared {1}').format(unicode(self.author.username), unicode(self.post.title[0:128]))

    class Meta:
        verbose_name = _('Share')
        verbose_name_plural = _('Shares')
        #prevent the same user being mentioned twice in a single comment or post
        #or well, being mentioned twice is ok, but sending twice the message is not
        unique_together = (('author', 'post'))
