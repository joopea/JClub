from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.models import create_base_model

from lib.cms.content_types import RichTextContent

from apps.cms.pages.content_types import RichTextImageContent


class Page(create_base_model(models.Model)):
    """
    Multi purpose CMS-page.
    """

    title = models.CharField(_("Title"), max_length=255)
    slug = models.SlugField(_('URL slug'), unique=True)
    language = models.ForeignKey('language.Language', limit_choices_to={'status': 'act'},
                                 to_field='name')

    class Meta:
        ordering = ('title', )
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return reverse("pages:detail", kwargs={'slug': self.slug})


# Register the FeinCMS templates
Page.register_regions(
    ('main', 'Main'),
)


Page.create_content_type(RichTextContent, regions=['main'])
Page.create_content_type(RichTextImageContent, regions=['main'])
