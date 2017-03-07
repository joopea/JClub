from django.db import models
from django.db.models import QuerySet


class ActiveQuerySet(QuerySet):
    def delete(self):
        self.update(active=False)


class ActiveManager(models.Manager):
    def active(self):
        return self.model.objects.filter(active=True)

    def get_query_set(self):
        return ActiveQuerySet(self.model, using=self._db)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(published=True)
