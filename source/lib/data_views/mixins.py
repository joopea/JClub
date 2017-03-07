from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.apps import apps as django_apps
from django.db import connections
from django.http import Http404

from lib.data_views.exceptions import MultipleRecordsReturned, RecordDoesNotExist, DataViewConfigError


class DataViewMultipleObjectMixin(object):

    cache_enabled = False

    @classmethod
    def list(cls, *args, **kwargs):
        """
        Your implementation for filtering objects i.e. model.objects.filter(..)
        This method always needs to return a QuerySet, even when empty

        Args:
            key: type - description
        Returns:
            type - description
        """

        result = cls.get_queryset().filter(*args, **kwargs)

        return result

    @classmethod
    def list_or_none(cls, *args, **kwargs):
        """
        Return a list of models instances

        Args:
            key: type - description
        Returns:
            type - description
        """
        result = cls.list(*args, **kwargs)
        if result.exists():
            return result
        else:
            return None


class DataViewSingleObjectMixin(object):

    cache_enabled = False

    @classmethod
    def get(cls, *args, **kwargs):
        """
        Your implementation for getting an object i.e models.objects.get(...)
        or cls.query().get(...)
        This method always needs to return either an object or None.

        Args:
            key: type - description
        Returns:
            type - description
        """

        try:
            result = cls.get_queryset().get(*args, **kwargs)
        except ObjectDoesNotExist, e:
            raise RecordDoesNotExist(e)
        except MultipleObjectsReturned:
            raise MultipleRecordsReturned("You borked your database, bitch")

        return result

    @classmethod
    def get_or_none(cls, *args, **kwargs):
        """
        Get a single instance of a model. If the query returns none, none
        will be returned

        Args:
            key: type - description
        Returns:
            type - description
        """
        try:
            return cls.get(*args, **kwargs)
        except RecordDoesNotExist:
            return None

    @classmethod
    def get_or_404(cls, *args, **kwargs):
        try:
            return cls.get(*args, **kwargs)
        except RecordDoesNotExist, e:
            raise Http404('{0} not found: {1}'.format(cls.model, str(kwargs)))


class DataViewSourceMixin(object):

    app_name = None
    model = None
    manager = 'objects'

    @classmethod
    def get_model(cls):
        """
        Get the registered model and return it.

        Returns:
            ModelBase - ModelBase of self.app_name + self.model
        """
        if not cls.app_name or not cls.model:
            raise DataViewConfigError(
                "Improperly configured: app_name or model not defined"
            )
        return django_apps.get_model(app_label=cls.app_name, model_name=cls.model)

    @classmethod
    def get_manager(cls):

        try:
            queryset_manager = getattr(cls.get_model(), cls.manager)
        except AttributeError:
            raise DataViewConfigError("Improperly configured manager for dataview")

        return queryset_manager

    @classmethod
    def get_queryset(cls):
        """
        Get a queryset for the registered model and return it

        Returns:
            Queryset - Configured manager (cls.manager) of self.app_name + self.model
        """

        return cls.get_manager()


class RawQueryMixin(object):
    @classmethod
    def raw(cls, query, connection='default'):
        cursor = connections[connection].cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
