from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withuser import WithAuthor


class Save(WithUpdates, WithAuthor, models.Model):

    post = models.ForeignKey('post.Post')

    def __unicode__(self):
        return '%s saved %s' % (unicode(self.author.username), unicode(self.post.title[0:128]))

    class Meta:
        verbose_name = _('Save')
        verbose_name_plural = _("Saves")
        unique_together = (('author', 'post'))
