"""Context cache — memory-only.

Caches PackInterpretationContext shells / context ids.
No BaZi logic. No Redis.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.cache.memory_cache import MemoryCache


class ContextCache(MemoryCache[Any]):
    """In-memory cache for interpretation context artifacts."""

    def __init__(self, *, max_size: int = 256, default_ttl_seconds: float | None = None) -> None:
        """Initialize context cache."""
        super().__init__(
            cache_id="context_cache",
            max_size=max_size,
            default_ttl_seconds=default_ttl_seconds,
        )
