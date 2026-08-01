"""Placeholder cache — memory-only.

Caches placeholder binding shells / opaque ids only.
No BaZi logic. No Redis.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.cache.memory_cache import MemoryCache


class PlaceholderCache(MemoryCache[Any]):
    """In-memory cache for placeholder reference bindings."""

    def __init__(self, *, max_size: int = 1024, default_ttl_seconds: float | None = None) -> None:
        """Initialize placeholder cache."""
        super().__init__(
            cache_id="placeholder_cache",
            max_size=max_size,
            default_ttl_seconds=default_ttl_seconds,
        )
