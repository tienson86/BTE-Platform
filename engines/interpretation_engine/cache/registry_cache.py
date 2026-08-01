"""Registry cache — memory-only.

Caches registry lookup results / registration descriptors.
No BaZi logic. No Redis.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.cache.memory_cache import MemoryCache


class RegistryCache(MemoryCache[Any]):
    """In-memory cache for registry descriptors and lookup results."""

    def __init__(self, *, max_size: int = 512, default_ttl_seconds: float | None = None) -> None:
        """Initialize registry cache."""
        super().__init__(
            cache_id="registry_cache",
            max_size=max_size,
            default_ttl_seconds=default_ttl_seconds,
        )
