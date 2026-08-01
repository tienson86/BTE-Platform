"""Generic in-memory cache implementation."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from time import monotonic
from typing import Any, Hashable

from engines.analysis_engine.cache.cache_policy import CachePolicy, EvictionPolicy
from engines.analysis_engine.exceptions.cache_error import CacheError


@dataclass(slots=True)
class _CacheRecord:
    """Internal cache record with optional expiry metadata."""

    value: Any
    created_at: float
    last_access_at: float
    expires_at: float | None


@dataclass(frozen=True, slots=True)
class CacheStats:
    """Immutable cache statistics snapshot."""

    hits: int
    misses: int
    size: int
    evictions: int
    expirations: int
    namespace: str

    def to_dict(self) -> dict[str, int | str]:
        """Return a JSON-compatible dictionary representation."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "size": self.size,
            "evictions": self.evictions,
            "expirations": self.expirations,
            "namespace": self.namespace,
        }


class MemoryCache:
    """Process-local memory cache with optional TTL and size limits.

    Memory only. No Redis, disk, or network backends.
    """

    def __init__(self, policy: CachePolicy | None = None) -> None:
        """Initialize an in-memory cache with the given policy."""
        self._policy = policy or CachePolicy.default()
        self._store: OrderedDict[Hashable, _CacheRecord] = OrderedDict()
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0

    @property
    def policy(self) -> CachePolicy:
        """Return the active cache policy."""
        return self._policy

    def get(self, key: Hashable) -> Any | None:
        """Return a cached value or None on miss/expiry."""
        if not self._policy.enabled:
            self._misses += 1
            return None
        record = self._store.get(key)
        if record is None:
            self._misses += 1
            return None
        if self._is_expired(record):
            del self._store[key]
            self._expirations += 1
            self._misses += 1
            return None
        now = monotonic()
        record.last_access_at = now
        if self._policy.eviction == EvictionPolicy.LRU:
            self._store.move_to_end(key)
        self._hits += 1
        return record.value

    def set(self, key: Hashable, value: Any) -> None:
        """Store a value in memory according to policy."""
        if not self._policy.enabled:
            return
        now = monotonic()
        expires_at = None
        if self._policy.ttl_seconds is not None:
            expires_at = now + self._policy.ttl_seconds
        self._store[key] = _CacheRecord(
            value=value,
            created_at=now,
            last_access_at=now,
            expires_at=expires_at,
        )
        if self._policy.eviction == EvictionPolicy.LRU:
            self._store.move_to_end(key)
        self._enforce_max_entries()

    def delete(self, key: Hashable) -> bool:
        """Delete a key. Return True if the key existed."""
        if key in self._store:
            del self._store[key]
            return True
        return False

    def contains(self, key: Hashable) -> bool:
        """Return True when a non-expired key is present."""
        return self.has(key)

    def has(self, key: Hashable) -> bool:
        """Return True when a non-expired key is present without hit/miss side effects."""
        record = self._store.get(key)
        if record is None:
            return False
        if self._is_expired(record):
            del self._store[key]
            self._expirations += 1
            return False
        return True

    def clear(self) -> None:
        """Remove all cached entries."""
        self._store.clear()

    def size(self) -> int:
        """Return the number of stored entries (including not-yet-purged expired)."""
        self._purge_expired()
        return len(self._store)

    def keys(self) -> tuple[Hashable, ...]:
        """Return current non-expired keys in store order."""
        self._purge_expired()
        return tuple(self._store.keys())

    def stats(self) -> CacheStats:
        """Return an immutable statistics snapshot."""
        return CacheStats(
            hits=self._hits,
            misses=self._misses,
            size=self.size(),
            evictions=self._evictions,
            expirations=self._expirations,
            namespace=self._policy.namespace,
        )

    def reset_stats(self) -> None:
        """Reset hit/miss/eviction/expiration counters."""
        self._hits = 0
        self._misses = 0
        self._evictions = 0
        self._expirations = 0

    def _is_expired(self, record: _CacheRecord) -> bool:
        """Return True when the record TTL has elapsed."""
        if record.expires_at is None:
            return False
        return monotonic() >= record.expires_at

    def _purge_expired(self) -> None:
        """Remove expired entries from the store."""
        expired = [key for key, record in self._store.items() if self._is_expired(record)]
        for key in expired:
            del self._store[key]
            self._expirations += 1

    def _enforce_max_entries(self) -> None:
        """Evict entries when max_entries is exceeded."""
        max_entries = self._policy.max_entries
        if max_entries is None:
            return
        while len(self._store) > max_entries:
            if self._policy.eviction == EvictionPolicy.FIFO:
                self._store.popitem(last=False)
            elif self._policy.eviction == EvictionPolicy.LRU:
                self._store.popitem(last=False)
            else:
                raise CacheError(f"unsupported_eviction:{self._policy.eviction}")
            self._evictions += 1
