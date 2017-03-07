import time
from django.core.cache import cache


class CacheNotFound(object):
    pass


class QuerysetDataViewCache(object):
    #process timeout limit
    CACHE_DOGPILE_TIMEOUT = 30
    CACHE_GRACE_PERIOD = 300

    #poison-pill, saving a None is perfectly valid and not a cache miss
    NOT_FOUND = CacheNotFound()

    def _get_cache(self, key):
        packed_val = cache.get(key)
        if packed_val is None:
            return self.NOT_FOUND
        val, refresh_time, refreshing = packed_val
        if (time.time() > refresh_time) and not refreshing:
            self._set_cache(key, val, self.CACHE_DOGPILE_TIMEOUT, refreshing=True)
            return self.NOT_FOUND
        return val

    def _set_cache(self, key, val, timeout, refreshing=False):
        refresh_time = time.time() + timeout
        cache_timeout = timeout + self.CACHE_GRACE_PERIOD
        if refreshing:
            #dont wait for the grace period again when refreshing
            cache_timeout = timeout + self.CACHE_DOGPILE_TIMEOUT
        packed_val = (val, refresh_time, refreshing)
        return cache.set(key, packed_val, cache_timeout)

    def _del_cache(self, key):
        return cache.delete(key)
