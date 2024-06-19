#!/usr/bin/env python3
""" Defines `Cache` class """

import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """ To use Redis """
    def __init__(self):
        """ Initialization """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ To set random-generated key to data """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ To get the value for a specific key """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key):
        """ Automatically parametrize `Cache.get` with string conversion """
        return self._redis.get(key).decode("utf-8")

    def get_int(self, key):
        """ Automatically parametrize `Cache.get` with integer conversion """
        return self._redis.get(key, int)
