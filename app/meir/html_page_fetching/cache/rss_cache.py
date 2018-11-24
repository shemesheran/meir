from cachetools import TTLCache

class RSSCache:

    def __init__(self, cache_max_size, cache_ttl_seconds):
        self.cache = TTLCache(ttl=cache_ttl_seconds, maxsize=cache_max_size)

    def update_cache(self, key, value):
        self.cache.update({key: value})

    def get_from_cache(self, key):
        return self.cache.get(key)