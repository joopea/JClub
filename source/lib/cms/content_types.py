"""
FeinCMS content types. For documentation see http://feincms-django-cms.readthedocs.org/en/latest/contenttypes.html
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from feincms.contrib.richtext import RichTextField
from feincms.content.richtext import models as cms_models
from feincms_oembed.models import CachedLookup

from apps.core.utils import FileBrowserImageSize
from lib.behaviours.models.withimage import WithImage


class RichTextContent(cms_models.RichTextContent):

    def render(self, **kwargs):
        return render_to_string(
            'cms/rich_text_content.html',
            {'content': self},
            context_instance=kwargs.get('context'))

    class Meta:
        abstract = True
        verbose_name = _('Rich text')
        verbose_name_plural = _('Rich texts')


class ImageContent(WithImage, models.Model):
    """
    Page image content-type

    (Havings problems with django model inheritance and feincms. Have to declare the model as is)
    """

    template = 'cms/image_content.html'
    image_size = FileBrowserImageSize.PAGE_LARGE  # Filebrowser thumbnail size.

    alt_text = models.CharField(_('Alternative Text'), max_length=255, blank=True, help_text=_('Description of the image'))
    # caption = models.CharField(_('Titel'), max_length=255, blank=True)

    def get_image(self):
        return self.image.version_generate(self.image_size)

    def render(self, **kwargs):
        templates = [self.template]
        return render_to_string(
            templates,
            {'content': self},
            context_instance=kwargs.get('context'),
        )

    @classmethod
    def initialize_type(cls, POSITION_CHOICES=None, FORMAT_CHOICES=None):
        if POSITION_CHOICES:
            models.CharField(
                _('position'),
                max_length=10,
                choices=POSITION_CHOICES,
                default=POSITION_CHOICES[0][0]
            ).contribute_to_class(cls, 'position')

    class Meta:
        abstract = True
        verbose_name = _('Image')
        verbose_name_plural = _('Images')



class RichTextImageContent(WithImage, models.Model):
    POSITION_CHOICES = (
	('center', _('Center')),
        ('left', _('Left')),
        ('right', _('Right')),
    )

    template = 'cms/image_text_content.html'
    image_size = FileBrowserImageSize.PAGE_SMALL  # Filebrowser thumbnail size.

    alt_text = models.CharField(_('Alternative Text'), max_length=255, blank=True, help_text=_('Description of the image'))
    # caption = models.CharField(_('Titel'), max_length=255, blank=True)
    text = RichTextField(_('Text'), blank=True)

    def get_image(self):
        return self.image.version_generate(self.image_size)

    def render(self, **kwargs):
        templates = [self.template]
        return render_to_string(
            templates,
            {'content': self},
            context_instance=kwargs.get('context'),
        )

    @classmethod
    def initialize_type(cls, POSITION_CHOICES=None, FORMAT_CHOICES=None):
        if POSITION_CHOICES:
            models.CharField(
                'position',
                max_length=10,
                choices=POSITION_CHOICES,
                default=POSITION_CHOICES[0][0]
            ).contribute_to_class(cls, 'position')

    class Meta:
        abstract = True
        verbose_name = _('Rich text with image')
        verbose_name_plural = _('Rich texts with image')


class OembedContent(models.Model):
    """
    Content type for integrating anything supported by Embed.ly and beyond into the CMS
    """

    TYPE_CHOICES = [
        ('default', _('Standard'), {
            'maxwidth': 640, 'maxheight': 360, 'wmode': 'opaque'}),
    ]

    url = models.URLField(
        _('URL'),
        help_text=_(
            'Enter the URL of the content that needs to be embedded, '
            'example: http://www.youtube.com/watch?v=Nd-vBFJN_2E'
        ),
    )

    @classmethod
    def initialize_type(cls, TYPE_CHOICES, PARAMS={}):
        choices = [row[0:2] for row in TYPE_CHOICES]
        cls.add_to_class(
            'type',
            models.CharField(
                'type',
                max_length=20,
                choices=choices,
                default=choices[0][0],
            )
        )
        cls._type_config = dict((row[0], row[2]) for row in TYPE_CHOICES)
        cls._params = PARAMS

    def get_templates(self, embed):
        """
        Plugin Embedding system with templates:

        To override or extend Embed.ly embed rendering, simply declare a template with
        the given provider name (like oembed_[provider_name]). This template can be used
        to render embed data as pleased.

        Do not override type or default templates, unless you know what you are doing.
        """

        return [
            'cms/oembed_%s.html' % embed.get('provider_name', '').lower(),
            'cms/oembed_%s.html' % embed.get('type', '').lower(),
            'cms/oembed_content.html',
        ]


    def get_html_from_json(self, fail_silently=False):
        params = self._type_config.get(self.type, {})
        params.update(self._params)

        try:
            embed = CachedLookup.objects.oembed(self.url, **params)
        except TypeError:
            if fail_silently:
                return u''
            raise ValidationError(
                _('I don\'t know how to embed %s.') % self.url)

        return render_to_string(
            self.get_templates(embed),
            {'response': embed, 'content': self}
        )

    def clean(self, *args, **kwargs):
        self.get_html_from_json()

    def render(self, **kwargs):
        return self.get_html_from_json(fail_silently=True)

    class Meta:
        abstract = True
        verbose_name = _('Embedded content')
        verbose_name_plural = _('Embedded content')
