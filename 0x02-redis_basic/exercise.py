#!/usr/bin/env python3
""" Defines `Cache` class """

import redis
import uuid
from typing import Union


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
