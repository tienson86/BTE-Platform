"""Sentence cache — memory-only.

Caches sentence-ref descriptors only (no NLG bodies).
No BaZi logic. No Redis.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.cache.memory_cache import MemoryCache


class SentenceCache(MemoryCache[Any]):
    """In-memory cache for sentence reference descriptors."""

    def __init__(self, *, max_size: int = 1024, default_ttl_seconds: float | None = None) -> None:
        """Initialize sentence cache."""
        super().__init__(
            cache_id="sentence_cache",
            max_size=max_size,
            default_ttl_seconds=default_ttl_seconds,
        )
