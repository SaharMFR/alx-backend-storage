#!/usr/bin/env python3
""" Defines `Cache` class """

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Counts how many times methods of the `Cach`e class are called """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Calls history """
    @wraps(method)
    def wrapper(self, *args, **kargs):
        """ wrapper """
        key = method.__qualname__
        inputs = key + ":inputs"
        outputs = key + ":outputs"
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kargs)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def replay(function: Callable):
    """ Display the history of calls of a particular function """
    r = redis.Redis()
    key = function.__qualname__
    inputs = r.lrange(key + ":inputs", 0, -1)
    outputs = r.lrange(key + ":outputs", 0, -1)
    nCalls = len(inputs)

    times = "times"
    if nCalls == 1:
        times = "time"

    fun_str = key + " was called " + nCalls + " " + times + ":"
    print(fun_str)
    for k, v in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(key, k.decode("utf-8"),
                                     v.decode("utf-8")))


class Cache:
    """ To use Redis """
    def __init__(self):
        """ Initialization """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
