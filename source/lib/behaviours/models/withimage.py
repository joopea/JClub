from django.db import models
from filer.fields.image import FilerImageField


class WithImage(models.Model):
    image = FilerImageField(null=True, max_length=255, blank=True, related_name="+")

    class Meta:
        abstract = True


class WithIcon(models.Model):
    icon = FilerImageField(related_name="+", null=True, blank=True, max_length=255)

    class Meta:
        abstract = True
