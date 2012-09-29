
import time

class Cache(object):
    
    def __init__(self, ttl):
        self.items = {}
        self.ttl = ttl

    def set(self, key, val):
        self.items[key] = (val, time.time())

    def get(self, key):
        val, touched_on = self.items.get(key, (None, None))

        if touched_on is None or time.time() - touched_on > self.ttl:
            raise KeyError(key)

        return val

    def cached(self, func):
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            try:
                return self.get(key)
            except KeyError:
                val = func(*args, **kwargs)
                self.set(key, val)
                return val

        return wrapper
