# api_client_generator/utils/caching.py

from functools import wraps
from typing import Callable, Any
import time

class Cache:
    def __init__(self):
        self._cache = {}

    def set(self, key: str, value: Any, expire: int = 0):
        self._cache[key] = (value, time.time() + expire if expire else None)

    def get(self, key: str) -> Any:
        if key in self._cache:
            value, expire = self._cache[key]
            if expire is None or expire > time.time():
                return value
            else:
                del self._cache[key]
        return None

    def clear(self):
        self._cache.clear()

def cached(expire: int = 0):
    def decorator(func: Callable):
        cache = Cache()

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            result = cache.get(key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(key, result, expire)
            return result

        return wrapper

    return decorator

# Usage:
# @cached(expire=60)
# def get_user(user_id: int):
#     # API call here
#     pass