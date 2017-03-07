from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class WithRichTextContent(models.Model):
    original_message = models.CharField(max_length=6144, db_index=True)
    message = RichTextField(_('Message'), max_length=6144)

    class Meta:
        abstract = True
