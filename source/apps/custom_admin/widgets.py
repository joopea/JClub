from django.contrib.admin.widgets import ForeignKeyRawIdWidget, ManyToManyRawIdWidget
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_unicode
from django.utils.html import escape


class VerboseForeignKeyRawIdWidget(ForeignKeyRawIdWidget):

    def __init__(self, rel, admin_site, manager='', attrs=None, using=None):
        self.manager = manager
        super(VerboseForeignKeyRawIdWidget, self).__init__(rel, admin_site, attrs, using)

    def get_manager(self):
        try:
            return getattr(self.rel.to, self.manager)
        except AttributeError:
            return self.rel.to._default_manager.using(self.db)

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        try:
            obj = self.get_manager().get(**{key: value})
            change_url = reverse(
                "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                args=(obj.pk,)
            )
            return '&nbsp;<strong><a href="%s">%s</a></strong>' % (change_url, escape(obj))
        except (ValueError, self.rel.to.DoesNotExist):
            return '???'


class VerboseManyToManyRawIdWidget(ManyToManyRawIdWidget):

    def __init__(self, rel, admin_site, manager='', attrs=None, using=None):
        self.manager = manager
        super(VerboseManyToManyRawIdWidget, self).__init__(rel, admin_site, attrs, using)

    def get_manager(self):
        try:
            return getattr(self.rel.to, self.manager)
        except AttributeError:
            return self.rel.to._default_manager.using(self.db)

    def label_for_value(self, value):
        values = value.split(',')
        str_values = []
        key = self.rel.get_related_field().name
        for v in values:
            try:
                obj = self.get_manager().get(**{key: v})
                x = smart_unicode(obj)
                change_url = reverse(
                    "admin:%s_%s_change" % (obj._meta.app_label, obj._meta.object_name.lower()),
                    args=(obj.pk,)
                )
                str_values += ['<strong><a href="%s">%s</a></strong>' % (change_url, escape(x))]
            except self.rel.to.DoesNotExist:
                str_values += [u'???']
        return u', '.join(str_values)
