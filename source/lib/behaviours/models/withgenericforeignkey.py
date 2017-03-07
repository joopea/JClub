from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class WithGenericForeignKey(models.Model):

    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType)

    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
