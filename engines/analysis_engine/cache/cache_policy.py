"""In-memory cache policy contracts."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from engines.analysis_engine.exceptions.cache_error import CacheError


class EvictionPolicy(str, Enum):
    """Supported in-memory eviction strategies."""

    LRU = "lru"
    FIFO = "fifo"


@dataclass(frozen=True, slots=True)
class CachePolicy:
    """Immutable policy for memory-only cache behavior.

    No external cache backends are supported.
    """

    enabled: bool = True
    max_entries: int | None = 1024
    ttl_seconds: float | None = None
    eviction: EvictionPolicy = EvictionPolicy.LRU
    namespace: str = "default"

    def __post_init__(self) -> None:
        """Validate policy constraints."""
        if self.max_entries is not None and self.max_entries < 1:
            raise CacheError("cache_max_entries_invalid")
        if self.ttl_seconds is not None and self.ttl_seconds <= 0:
            raise CacheError("cache_ttl_seconds_invalid")

    @classmethod
    def default(cls) -> CachePolicy:
        """Return the default in-memory cache policy."""
        return cls()

    @classmethod
    def disabled(cls) -> CachePolicy:
        """Return a disabled cache policy."""
        return cls(enabled=False, max_entries=None, ttl_seconds=None)
