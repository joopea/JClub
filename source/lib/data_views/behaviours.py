from lib.data_views.exceptions import DataViewConfigError


class QuerysetAble(object):
    queryset = None

    @classmethod
    def get_model(cls):
        """
        Get the model from the queryset and return it
        :return: The model instance of the queryset
        """
        if cls.queryset is None:
            raise DataViewConfigError("No queryset is configured")

        return cls.queryset.model

    @classmethod
    def get_queryset(cls):
        """
        Get the registered queryset and return it

        Returns:
            Queryset - Configured manager (cls.manager) of self.app_name + self.model
        """

        if cls.queryset is None:
            raise DataViewConfigError("No queryset is configured")

        return cls.queryset.clone()
