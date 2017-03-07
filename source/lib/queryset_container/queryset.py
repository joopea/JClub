import operator
import time

from django.core.cache import cache
from django.db.models import ObjectDoesNotExist

from .cache import QuerysetDataViewCache
from apps.post.models import Post


class CacheNotFound(object):
    pass


class __DataViewCache(object):
    #poison-pill, saving a None is perfectly valid and not a cache miss
    NOT_FOUND = CacheNotFound()
    TIMEOUT = 31536000

    #process timeout limit
    CACHE_DOGPILE_TIMEOUT = 30
    CACHE_GRACE_PERIOD = 300

    def get_cache(self, key):
        packed_val = cache.get(key)
        if packed_val is None:
            return self.NOT_FOUND
        val, refresh_time, refreshing = packed_val
        if (time.time() > refresh_time) and not refreshing:
            self.set_cache(key, val, self.CACHE_DOGPILE_TIMEOUT, refreshing=True)
            return self.NOT_FOUND
        return val

    def get_cache_many(self, keys):
        ret_values = cache.get_many(keys)
        #find missing and unpack+verify retrieved values
        values = {}
        missing = []
        for key in keys:
            # none value or cache miss
            packed_value = ret_values.get(key, None)
            if packed_value is None:
                missing.append(key)
                continue
            val, refresh_time, refreshing = packed_value
            values[key] = val
            #stale cache, re-set the cache with the dogpile timeout ang add it to the missing values
            if (time.time() > refresh_time) and not refreshing:
                self.set_cache(key, val, self.CACHE_DOGPILE_TIMEOUT, refreshing=True)
                missing.append(key)
                continue
        return [values, missing]

    def set_cache(self, key, val, timeout, refreshing=False):
        refresh_time = time.time() + timeout
        cache_timeout = timeout + self.CACHE_GRACE_PERIOD
        if refreshing:
            #dont wait for the grace period again when refreshing
            cache_timeout = timeout + self.CACHE_DOGPILE_TIMEOUT
        packed_val = (val, refresh_time, refreshing)
        return cache.set(key, packed_val, cache_timeout)

    def del_cache(self, key):
        return cache.delete(key)


class __ObjectDataViewCache(__DataViewCache):
    pass


class __ListDataViewCache(__DataViewCache):
    pass


class __ObjectDataView(__ObjectDataViewCache):
    """
    gets a single object (possibly with related data and modified fields-list)
        from a write-trough cache

    one class is created per query, that class knows the basis of its cache-key
    each of these classes are registered at the save/update signal of their models
        upon save and update a new cache entry is created
    """
    model = Post
    key = "id={id}"

    def generate_key(self, **kwargs):
        return self.model.__name__ + '|' + self.key.format(**kwargs)

    def get(self, **kwargs):
        """
        get the single object from cache, or from backend store
            returns the post-processed object trough get_object
        """
        key = self.generate_key(**kwargs)
        value = self.get_cache(key)
        if value is self.NOT_FOUND:
            value = self.generate_cache(**kwargs)
        return self.get_object(value, **kwargs)

    def get_object(self, value, **kwargs):
        return value

    def get_objects(self, values, args):
        collector = []
        for value, kwargs in zip(values, args):
            collector.append(self.get_object(value, **kwargs))
        return collector

    def get_many(self, items):
        keys = []
        key_arg_map = []
        key_arg_dict = {}
        for item in items:
            key = self.generate_key(**item)
            keys.append(key)
            key_arg_map.append((key, item))
            key_arg_dict[key] = item
        values, misses = self.get_cache_many(keys)
        missing_map = []
        for miss in misses:
            missing_map.append((miss, key_arg_dict[miss]))
            self.get_misses(values, missing_map)
        #finally we sort the values in the same order as we received the items
        ret_list = []
        for key, args in key_arg_map:
            ret_list.append(values[key])
        return self.get_objects(ret_list, items)

    def get_misses(self, values, misses):
        for i, kwargs in misses:
            values[i] = self.generate_cache(**kwargs)

    def generate_cache(self, **kwargs):
        instance = self.generate_cache_object(**kwargs)
        key = self.generate_key(**kwargs)
        self.set_cache(key, instance, self.TIMEOUT)
        return instance

    def clean_cache(self, **kwargs):
        self.del_cache(self.generate_key(**kwargs))
        return self

    def generate_cache_object(self, **kwargs):
        try:
            return self.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return self.model.objects.none()


class __ListDataView(__ListDataViewCache):

    pass


class __QuerysetDataView(QuerysetDataViewCache):
    #60 * 60 * 24 * 365 => one year
    TIMEOUT = 31536000
    object = None
    object_key = 'pk'

    def get_key(self, **kwargs):
        items = sorted(kwargs.items(), key=operator.itemgetter(0))
        key = self.__class__.__name__ + '|'
        for item in items:
            key += "%s=%s|" % item
        return key

    def get(self, **kwargs):
        """
        get from cache
            if miss, generate
        """
        key = self.get_key(**kwargs)
        value = self._get_cache(key)
        if value is self.NOT_FOUND:
            value = self.generate_cache(**kwargs)
        return self.get_object(value, **kwargs)

    def clean_cache(self, **kwargs):
        self._del_cache(self.get_key(**kwargs))
        return self

    def generate_cache(self, **kwargs):
        value = self.generate_cache_object(**kwargs)
        key = self.get_key(**kwargs)
        self._set_cache(key, value, self.TIMEOUT)
        return value

    def generate_cache_object(self, **kwargs):
        return None

    def get_object(self, value, **kwargs):
        """
        convert the cache into a use-able object
            useful when for example an id is cached but we need the object that id belongs to
            possibly from another cache
        """
        if value is None:
            return None
        if self.object is None:
            return value

        def inner_get_object(inner_obj):
            if len(inner_obj):
                return self.object().get(**{self.object_key: getattr(inner_obj, self.object_key)})
            else:
                return self.object().get()

        if isinstance(value, list):
            return [inner_get_object(obj) for obj in value]
        else:
            return inner_get_object(value)
        # return self.object().get(**{self.object_key: getattr(value, self.object_key)})


###########
###########
###########
###########
###########
###########
###########
###########
from datetime import datetime


class DataQuery(object):
    model = None
    key = 'pk'
    object_model = None
    object_key = 'pk'
    instance_key = 'pk'
    manager = 'objects'

    def get(self, **kwargs):
        try:
            instance = getattr(self.model, self.manager).get(**kwargs)
            if self.object_model:
                return self.get_object(instance)
            return instance
        except ObjectDoesNotExist:
            model = self.object_model or self.model
            return model[self.manager].none()

    def get_list(self, **kwargs):
        try:
            instances = getattr(self.model, self.manager).filter(**kwargs)
            if self.object_model:
                return self.get_objects(instances)
            return instances
        except ObjectDoesNotExist:
            return []

    def get_many(self, keys):
        instances = getattr(self.model, self.manager)\
            .filter(**{(self.key + '__in'): keys})
        if self.object_model:
            return self.get_object(instances)
        return instances

    def get_object(self, instance):
        return getattr(self.model, self.manager)\
            .get(**{self.object_key: getattr(instance, self.instance_key)})

    def get_objects(self, instances):
        return [self.get_object(instance) for instance in instances]


#@TODO add signal updaters to the CollectionQuery classes
class CollectionQuery(DataQuery):
    start = datetime.now()
    length = 20
    limit_key = 'created'
    last_item = 1

    def __init__(self):
        self._data = None

    def get(self, **kwargs):
        if self._data is None:
            self._data = self.get_data(**kwargs)
            length = len(self._data)
            if length > 0:
                self.last_item = getattr(self._data[len(self._data) - 1], self.limit_key)
        return self._data

    def get_data(self, **kwargs):
        raise NotImplementedError()

    def limit(self, start, length):
        if start != 1:
            self.start = start
        self.length = length
        return self

    def order_by(self, *args):
        #@TODO implement me :D, use this data for a smarter get_many """ self.limit_key + '__lt' """
        pass

    def get_from_store(self, **kwargs):
        return self.model.objects.filter(**kwargs)

    def get_many(self, keys):
        return super(CollectionQuery, self)\
            .get_many(keys)\
            .filter(**{(self.limit_key + '__lt'): str(self.start)})[:self.length]


