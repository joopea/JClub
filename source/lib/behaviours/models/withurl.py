from django.core.urlresolvers import reverse
from django.db import models


class WithAbsoluteUrl(models.Model):
    """
    For custom url argument to resolve a detail view use: _url_detail_field and _url_detail_value
    and declare the field in string format.
    """

    detail_view_name = 'detail'

    @property
    def _url_app_label(self):
        return self._meta.app_label

    def get_absolute_url(self):
        name = '{app_label}:{view_name}'.format(app_label=self._url_app_label, view_name=self.detail_view_name)
        kwargs = {'pk': self.pk}
        if hasattr(self.__class__, 'slug') and isinstance(self.__class__.slug, models.Field):
            kwargs = {'slug': self.slug}
        if hasattr(self.__class__, '_url_detail_field') and hasattr(self.__class__, '_url_detail_value'):
            kwargs = {self._url_detail_field: getattr(self, self._url_detail_value)}
        return reverse(name, kwargs=kwargs)

    class Meta:
        abstract = True