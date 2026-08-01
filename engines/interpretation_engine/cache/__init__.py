"""Cache architecture package.

Memory-only caches for Pack 03 runtime.
Re-exports legacy ``InterpretationCache`` for backward compatibility.
"""

from __future__ import annotations

from engines.interpretation_engine.cache.cache_interface import InterpretationCacheInterface
from engines.interpretation_engine.cache.cache_manager import CacheManager
from engines.interpretation_engine.cache.context_cache import ContextCache
from engines.interpretation_engine.cache.memory_cache import CacheStats, MemoryCache
from engines.interpretation_engine.cache.placeholder_cache import PlaceholderCache
from engines.interpretation_engine.cache.registry_cache import RegistryCache
from engines.interpretation_engine.cache.sentence_cache import SentenceCache
from engines.interpretation_engine.cache.template_cache import TemplateCache
from engines.interpretation_engine.legacy_runtime.cache import InterpretationCache

__all__ = [
    "CacheManager",
    "CacheStats",
    "ContextCache",
    "InterpretationCache",
    "InterpretationCacheInterface",
    "MemoryCache",
    "PlaceholderCache",
    "RegistryCache",
    "SentenceCache",
    "TemplateCache",
]
