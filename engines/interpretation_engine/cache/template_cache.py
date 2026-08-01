"""Template cache — memory-only.

Caches template-ref descriptors only (no template bodies).
No BaZi logic. No Redis.
"""

from __future__ import annotations

from typing import Any

from engines.interpretation_engine.cache.memory_cache import MemoryCache


class TemplateCache(MemoryCache[Any]):
    """In-memory cache for template reference descriptors."""

    def __init__(self, *, max_size: int = 512, default_ttl_seconds: float | None = None) -> None:
        """Initialize template cache."""
        super().__init__(
            cache_id="template_cache",
            max_size=max_size,
            default_ttl_seconds=default_ttl_seconds,
        )
