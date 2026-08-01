"""In-memory cache primitives for Pack 03.

No Redis. Memory cache only. Dependency Injection only.
Infrastructure only — no BaZi logic.
"""

from __future__ import annotations

import logging
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Generic, TypeVar

from engines.interpretation_engine.cache.cache_interface import InterpretationCacheInterface

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class CacheStats:
    """Immutable cache statistics snapshot."""

    hits: int = 0
    misses: int = 0
    sets: int = 0
    deletes: int = 0
    evictions: int = 0
    size: int = 0
    attributes: dict[str, Any] = field(default_factory=dict)

    @property
    def hit_ratio(self) -> float:
        """Return hit ratio in ``[0.0, 1.0]``."""
        total = self.hits + self.misses
        if total <= 0:
            return 0.0
        return self.hits / total

    def validate(self) -> bool:
        """Validate stats structural integrity."""
        return (
            self.hits >= 0
            and self.misses >= 0
            and self.sets >= 0
            and self.deletes >= 0
            and self.evictions >= 0
            and self.size >= 0
        )


@dataclass(slots=True)
class _CacheEntry(Generic[T]):
    """Internal cache entry with optional expiry."""

    value: T
    expires_at: float | None = None

    def is_expired(self, *, now: float | None = None) -> bool:
        """Return True when entry TTL has elapsed."""
        if self.expires_at is None:
            return False
        current = time.monotonic() if now is None else now
        return current >= self.expires_at


class MemoryCache(InterpretationCacheInterface, Generic[T]):
    """Bounded in-memory cache with optional TTL and LRU eviction."""

    def __init__(
        self,
        *,
        cache_id: str,
        max_size: int = 1024,
        default_ttl_seconds: float | None = None,
    ) -> None:
        """Initialize an empty memory cache.

        Args:
            cache_id: Diagnostic identifier.
            max_size: Maximum entries before LRU eviction (``<=0`` means unbounded).
            default_ttl_seconds: Optional default TTL applied on ``set``.
        """
        if not cache_id:
            raise ValueError("cache_id_required")
        self.cache_id = cache_id
        self._max_size = max_size
        self._default_ttl_seconds = default_ttl_seconds
        self._entries: OrderedDict[str, _CacheEntry[T]] = OrderedDict()
        self._hits = 0
        self._misses = 0
        self._sets = 0
        self._deletes = 0
        self._evictions = 0

    def get(self, key: str) -> T | None:
        """Return a cached value if present and not expired."""
        if not key:
            self._misses += 1
            return None
        entry = self._entries.get(key)
        if entry is None:
            self._misses += 1
            return None
        if entry.is_expired():
            self._entries.pop(key, None)
            self._misses += 1
            self._evictions += 1
            return None
        self._entries.move_to_end(key)
        self._hits += 1
        return entry.value

    def set(self, key: str, value: T, *, ttl_seconds: float | None = None) -> None:
        """Store a value in memory cache."""
        if not key:
            raise ValueError("cache_key_required")
        ttl = self._default_ttl_seconds if ttl_seconds is None else ttl_seconds
        expires_at = None
        if ttl is not None:
            if ttl < 0:
                raise ValueError("cache_ttl_invalid")
            expires_at = time.monotonic() + ttl
        self._entries[key] = _CacheEntry(value=value, expires_at=expires_at)
        self._entries.move_to_end(key)
        self._sets += 1
        self._evict_if_needed()
        logger.debug(
            "cache_set",
            extra={"cache_id": self.cache_id, "key": key, "size": len(self._entries)},
        )

    def delete(self, key: str) -> bool:
        """Delete a key if present. Return True when removed."""
        removed = self._entries.pop(key, None) is not None
        if removed:
            self._deletes += 1
        return removed

    def has(self, key: str) -> bool:
        """Return True when key exists and is not expired."""
        if not key:
            return False
        entry = self._entries.get(key)
        if entry is None:
            return False
        if entry.is_expired():
            self._entries.pop(key, None)
            self._evictions += 1
            return False
        return True

    def clear(self) -> None:
        """Clear all entries."""
        self._entries.clear()
        logger.info("cache_cleared", extra={"cache_id": self.cache_id})

    def size(self) -> int:
        """Return current entry count (includes unexpired only after purge)."""
        self.purge_expired()
        return len(self._entries)

    def keys(self) -> tuple[str, ...]:
        """Return current keys in LRU order (oldest first)."""
        self.purge_expired()
        return tuple(self._entries.keys())

    def purge_expired(self) -> int:
        """Remove expired entries; return eviction count."""
        now = time.monotonic()
        expired = [key for key, entry in self._entries.items() if entry.is_expired(now=now)]
        for key in expired:
            self._entries.pop(key, None)
            self._evictions += 1
        return len(expired)

    def stats(self) -> CacheStats:
        """Return statistics snapshot."""
        return CacheStats(
            hits=self._hits,
            misses=self._misses,
            sets=self._sets,
            deletes=self._deletes,
            evictions=self._evictions,
            size=len(self._entries),
            attributes={"cache_id": self.cache_id, "max_size": self._max_size},
        )

    def validate(self) -> bool:
        """Validate cache configuration readiness."""
        return bool(self.cache_id)

    def _evict_if_needed(self) -> None:
        """Evict least-recently-used entries when over capacity."""
        if self._max_size <= 0:
            return
        while len(self._entries) > self._max_size:
            self._entries.popitem(last=False)
            self._evictions += 1
