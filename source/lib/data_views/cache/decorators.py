import unicodedata
from django.core.cache import cache
import pickle

from lib.data_views.exceptions import DataViewCacheTTLError


class DataViewCacheDecorator(object):
    """
    How to cache query set results in django is as following:

    https://docs.djangoproject.com/en/1.7/ref/models/querysets/#pickling-querysets
    >>> import pickle
    >>> query = pickle.loads(s)  # Assuming 's' is the pickled string.
    >>> qs = MyModel.objects.all()
    >>> qs.query = query  # Restore the original 'query'.

    To use with DataViews, a DataView has a method to return a queryset (the view on the data)

    at the entry of the method, we should check if we can find a cache-entry for this request
    to determine the request a hash fo the arguments, the app_name, and the model_name is made

    at leaving the method, and if there was no cache to be found, we will cache the results
    using the same hashing methods for the next visit of the method.
    """

    def __init__(self, fn, ttl=None, cache_key=None):
        self.fn = fn

        if not isinstance(ttl, (int, long)):
            raise DataViewCacheTTLError("Cache TTL should be integer.")

        self.ttl = ttl
        self.cache_key = cache_key

    def __call__(self, *args, **kwargs):
        cache_key = self.get_cache_key(*args, **kwargs)
        data = None
        result = cache.get(cache_key)

        if result:
            #get class ref
            qs = self.fn.im_self.get_queryset()
            qs.query = pickle.loads(result)
            data = qs

        if not data:
            data = self.fn()

            pickled_result = pickle.dumps(result)
            cache.set(cache_key, pickled_result, self.ttl)

        return result

    def get_cache_key(self, *args, **kwargs):
        cache_key = self.cache_key
        if cache_key is None:
            cache_key = self.create_cache_key(*args, **kwargs)
        return cache_key

    def create_cache_key(self, *args, **kwargs):
        key = ".".join('{0}:{1}'.format(
            str(key), str(value)) for key, value in kwargs.iteritems())
        cache_key = '{0}:{1}'.format(self.fn.im_self.__name__, key)
        return "".join(
            ch for ch in unicode(cache_key) if (unicodedata.category(ch)[0] != "C" and unicodedata.category(ch)[0] != "Z")
        )