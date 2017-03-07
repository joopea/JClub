"""
FeinCMS content types. For documentation see http://feincms-django-cms.readthedocs.org/en/latest/contenttypes.html
"""

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.contrib.richtext import RichTextField

from lib.behaviours.models.withimage import WithImage


class RichTextImageContent(WithImage, models.Model):

    POSITION_CHOICES = (
        ('center', 'Center'),
        ('left', 'Left'),
        ('right', 'Right'),
    )

    template = 'cms/image_text_content.html'

    alt_text = models.CharField(_('Alternative Text'), max_length=255, blank=True, help_text=_('Description of the image'))
    text = RichTextField(_('Text'), blank=True)

    def render(self, **kwargs):
        templates = [self.template]
        return render_to_string(
            templates,
            {'content': self},
            context_instance=kwargs.get('context'),
        )

    @classmethod
    def initialize_type(cls, POSITION_CHOICES=POSITION_CHOICES, FORMAT_CHOICES=None):
        if POSITION_CHOICES:
            models.CharField('position',
                max_length=10,
                choices=POSITION_CHOICES,
                default=POSITION_CHOICES[0][0]
            ).contribute_to_class(cls, 'position')

    class Meta:
        abstract = True
        verbose_name = _('Rich text with image')
        verbose_name_plural = _('Rich texts with image')
