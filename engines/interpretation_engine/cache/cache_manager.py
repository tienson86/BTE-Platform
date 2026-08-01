"""Cache manager aggregating Pack 03 memory caches.

Dependency Injection only. No singleton. No Redis.
"""

from __future__ import annotations

import logging
from typing import Mapping

from engines.interpretation_engine.cache.context_cache import ContextCache
from engines.interpretation_engine.cache.memory_cache import CacheStats, MemoryCache
from engines.interpretation_engine.cache.placeholder_cache import PlaceholderCache
from engines.interpretation_engine.cache.registry_cache import RegistryCache
from engines.interpretation_engine.cache.sentence_cache import SentenceCache
from engines.interpretation_engine.cache.template_cache import TemplateCache

logger = logging.getLogger(__name__)


class CacheManager:
    """DI facade over context/sentence/template/placeholder/registry caches."""

    def __init__(
        self,
        *,
        context_cache: ContextCache | None = None,
        sentence_cache: SentenceCache | None = None,
        template_cache: TemplateCache | None = None,
        placeholder_cache: PlaceholderCache | None = None,
        registry_cache: RegistryCache | None = None,
    ) -> None:
        """Initialize with optional injected domain caches."""
        self._context = context_cache or ContextCache()
        self._sentence = sentence_cache or SentenceCache()
        self._template = template_cache or TemplateCache()
        self._placeholder = placeholder_cache or PlaceholderCache()
        self._registry = registry_cache or RegistryCache()

    @property
    def context(self) -> ContextCache:
        """Return context cache."""
        return self._context

    @property
    def sentence(self) -> SentenceCache:
        """Return sentence cache."""
        return self._sentence

    @property
    def template(self) -> TemplateCache:
        """Return template cache."""
        return self._template

    @property
    def placeholder(self) -> PlaceholderCache:
        """Return placeholder cache."""
        return self._placeholder

    @property
    def registry(self) -> RegistryCache:
        """Return registry cache."""
        return self._registry

    def caches(self) -> Mapping[str, MemoryCache[object]]:
        """Return all domain caches by id."""
        return {
            self._context.cache_id: self._context,
            self._sentence.cache_id: self._sentence,
            self._template.cache_id: self._template,
            self._placeholder.cache_id: self._placeholder,
            self._registry.cache_id: self._registry,
        }

    def clear_all(self) -> None:
        """Clear every domain cache."""
        for cache in self.caches().values():
            cache.clear()
        logger.info("cache_manager_cleared_all")

    def purge_expired(self) -> int:
        """Purge expired entries across all caches; return total evictions."""
        return sum(cache.purge_expired() for cache in self.caches().values())

    def stats(self) -> dict[str, CacheStats]:
        """Return stats for every domain cache."""
        return {cache_id: cache.stats() for cache_id, cache in self.caches().items()}

    def total_size(self) -> int:
        """Return combined entry count across domain caches."""
        return sum(cache.size() for cache in self.caches().values())

    def validate(self) -> bool:
        """Validate all domain caches are ready."""
        return all(cache.validate() for cache in self.caches().values())
