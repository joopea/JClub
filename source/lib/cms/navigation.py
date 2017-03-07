from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey

class BaseNavigationNode(PolymorphicMPTTModel):
    parent = PolymorphicTreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name='parent')

    class Meta:
        verbose_name = "Tree node"
        verbose_name_plural = "Tree nodes"
        abstract = True
