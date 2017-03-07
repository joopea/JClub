from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class PublishAble(models.Model):
    published = models.BooleanField(_('Published'), default=False)
    publish_date = models.DateTimeField(_('Publish date'), default=None, null=True)

    def set_published(self, to=True):
        # Todo: moved this method from the queryset (see below) because of accessiblilty problems
        self.published = to

        if to:
            self.publish_date = timezone.now()
        else:
            self.publish_date = None

    class Meta:
        abstract = True


class PublishAbleQueryset(QuerySet):

    def set_published(self, to=True):
        self.published = to

        if to:
            self.publish_date = timezone.now()
        else:
            self.publish_date = None
