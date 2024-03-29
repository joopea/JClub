from adminsortable.models import SortableMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from lib.behaviours.models.withupdates import WithUpdates
from lib.behaviours.models.withimage import WithImage, WithIcon
from apps.language.models import Language


class Community(WithImage, WithIcon, WithUpdates, SortableMixin, models.Model):

    name = models.CharField(_('Name'), max_length=255, default='', db_index=True)
    description = models.TextField(_('Description'), max_length=2048, default='', db_index=True)

    position = models.IntegerField(default=0, db_index=True, editable=False)
    language = models.ForeignKey('language.Language', default=settings.LANGUAGE_CODE, to_field='initial')

    def __unicode__(self):
        return unicode(self.name)


    class Meta:
        ordering = ('position', )
        verbose_name = _('Community')
        verbose_name_plural = _('Communities')

    def get_absolute_url(self):
        return reverse('wall:community', kwargs={'pk': self.pk})
    
    def valid_language(self):
        active_langs = Language.objects.filter(status='act')
        return self.language in active_langs
