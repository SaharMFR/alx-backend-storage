#!/usr/bin/env python3
""" Requests caching and tracking """

from functools import wraps
import redis
import requests
from typing import Callable

redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """ Caches the output of fetched data """
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """ The wrapper function for caching the output """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request.
    """
    req = requests.get(url)
    return req.text
