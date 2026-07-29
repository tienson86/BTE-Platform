from __future__ import annotations


class MatcherCache:

    def __init__(self):

        self._cache = {}

    def has(self, key):

        return key in self._cache

    def get(self, key):

        return self._cache.get(key)

    def put(self, key, value):

        self._cache[key] = value

    def clear(self):

        self._cache.clear()
