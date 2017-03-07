from lib.data_views.behaviours import QuerysetAble
from lib.data_views.mixins import DataViewSourceMixin, DataViewMultipleObjectMixin, DataViewSingleObjectMixin


class ModelDataView(DataViewSourceMixin, DataViewMultipleObjectMixin, DataViewSingleObjectMixin):

    pass


class QuerysetDataView(DataViewSourceMixin, QuerysetAble, DataViewMultipleObjectMixin, DataViewSingleObjectMixin):

    pass