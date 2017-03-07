from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from lib.utils.jalali import Gregorian


class WithUpdates(models.Model):
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now_add=True)

    @property
    def created_jalali(self):
        return Gregorian(self.created.strftime('%Y-%m-%d')).persian_string() + self.created.strftime(' %H:%M')

    @property
    def modified_jalali(self):
        return Gregorian(self.modified.strftime('%Y-%m-%d')).persian_string() + self.modified.strftime(' %H:%M')

    @property
    def created_greg(self):
        return Gregorian(self.created.strftime('%Y-%m-%d'))

    @property
    def modified_greg(self):
        return Gregorian(self.modified.strftime('%Y-%m-%d'))

    def save(self, *args, **kwargs):
        self.modified = timezone.now()
        super(WithUpdates, self).save(*args, **kwargs)

    class Meta:
        abstract = True
