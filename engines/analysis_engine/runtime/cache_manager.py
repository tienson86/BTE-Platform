"""Request-scoped and optional cross-request cache manager."""

from __future__ import annotations

import logging
from threading import RLock
from typing import Any, Hashable

from engines.analysis_engine.runtime.exceptions import CacheError

logger = logging.getLogger(__name__)


class CacheManager:
    """Runtime cache without semantic StageResult cross-request reuse by default.

    Request-scope cache lives for one Execution Unit.
    Cross-request cache is opt-in and must use full semantic keys.
    """

    def __init__(self, *, enable_cross_request: bool = False) -> None:
        self._enable_cross_request = enable_cross_request
        self._request_cache: dict[Hashable, Any] = {}
        self._cross_request_cache: dict[Hashable, Any] = {}
        self._lock = RLock()
        self.hits = 0
        self.misses = 0

    def get(self, key: Hashable, *, scope: str = "request") -> Any | None:
        """Return cached value or None on miss."""
        store = self._store(scope)
        with self._lock:
            if key in store:
                self.hits += 1
                logger.debug(
                    "cache_hit",
                    extra={"cache_scope": scope, "cache_key": repr(key)},
                )
                return store[key]
            self.misses += 1
            logger.debug(
                "cache_miss",
                extra={"cache_scope": scope, "cache_key": repr(key)},
            )
            return None

    def set(
        self,
        key: Hashable,
        value: Any,
        *,
        scope: str = "request",
    ) -> None:
        """Store a value in the selected cache scope."""
        if scope == "cross_request" and not self._enable_cross_request:
            raise CacheError(
                "Cross-request cache is disabled by policy",
                details={"key": repr(key)},
            )
        store = self._store(scope)
        with self._lock:
            store[key] = value

    def clear(self, *, scope: str | None = None) -> None:
        """Clear request cache, cross-request cache, or both."""
        with self._lock:
            if scope is None or scope == "request":
                self._request_cache.clear()
            if scope is None or scope == "cross_request":
                self._cross_request_cache.clear()

    def begin_request(self) -> None:
        """Reset request-scope cache for a new Execution Unit."""
        self.clear(scope="request")

    def end_request(self) -> None:
        """Drop request-scope cache at Execution Unit completion."""
        self.clear(scope="request")

    def snapshot_stats(self) -> dict[str, int]:
        """Return hit/miss counters."""
        with self._lock:
            return {"hits": self.hits, "misses": self.misses}

    def _store(self, scope: str) -> dict[Hashable, Any]:
        if scope == "request":
            return self._request_cache
        if scope == "cross_request":
            return self._cross_request_cache
        raise CacheError(
            f"Unknown cache scope: {scope}",
            details={"scope": scope},
        )
