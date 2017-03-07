

class DataViewException(Exception):
    pass


class DataViewCacheKeyError(DataViewException):
    pass


class DataViewCacheTTLError(DataViewException):
    pass


class DataViewConfigError(DataViewException):
    pass


class RecordDoesNotExist(DataViewException):
    pass


class MultipleRecordsReturned(DataViewException):
    pass
