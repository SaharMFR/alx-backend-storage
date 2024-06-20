#!/usr/bin/env python3
""" Requests caching and tracking """

import redis
from typing import Callable
from functools import wraps
import requests


redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """ Caches the output of fetched data """
    @wraps(method)
    def invoker(url) -> str:
        """ The wrapper function for caching the output """
        redis_store.incr(f"count:{url}")
        res = redis_store.get(f"result:{url}")
        if res:
            return res.decode("utf-8")
        res = method(url)
        redis_store.set(f"count:{url}", 0)
        redis_store.setex(f"result:{url}", 10, res)
        return res
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request.
    """
    return requests.get(url).text
