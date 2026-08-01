"""Cache manager facade for in-memory Analysis Engine caches."""

from __future__ import annotations

from typing import Any, Hashable, Mapping

from engines.analysis_engine.cache.cache_policy import CachePolicy
from engines.analysis_engine.cache.context_cache import ContextCache
from engines.analysis_engine.cache.memory_cache import CacheStats, MemoryCache
from engines.analysis_engine.cache.registry_cache import RegistryCache
from engines.analysis_engine.exceptions.cache_error import CacheError


class CacheManager:
    """Coordinate memory-only cache namespaces for Analysis Engine runtime.

    Distinct from ``runtime.cache_manager.CacheManager``.
    No external cache backends.
    """

    def __init__(self, policy: CachePolicy | None = None) -> None:
        """Initialize managed memory, context, and registry caches."""
        self._policy = policy or CachePolicy.default()
        self._memory = MemoryCache(
            CachePolicy(
                enabled=self._policy.enabled,
                max_entries=self._policy.max_entries,
                ttl_seconds=self._policy.ttl_seconds,
                eviction=self._policy.eviction,
                namespace="memory",
            )
        )
        self._context = ContextCache(
            CachePolicy(
                enabled=self._policy.enabled,
                max_entries=self._policy.max_entries,
                ttl_seconds=self._policy.ttl_seconds,
                eviction=self._policy.eviction,
                namespace="context",
            )
        )
        self._registry = RegistryCache(
            CachePolicy(
                enabled=self._policy.enabled,
                max_entries=self._policy.max_entries,
                ttl_seconds=self._policy.ttl_seconds,
                eviction=self._policy.eviction,
                namespace="registry",
            )
        )

    @property
    def policy(self) -> CachePolicy:
        """Return the root cache policy."""
        return self._policy

    @property
    def memory(self) -> MemoryCache:
        """Return the generic memory cache."""
        return self._memory

    @property
    def context(self) -> ContextCache:
        """Return the context cache."""
        return self._context

    @property
    def registry(self) -> RegistryCache:
        """Return the registry cache."""
        return self._registry

    def get(self, key: Hashable) -> Any | None:
        """Get a value from the generic memory cache."""
        return self._memory.get(key)

    def set(self, key: Hashable, value: Any) -> None:
        """Set a value in the generic memory cache."""
        self._memory.set(key, value)

    def delete(self, key: Hashable) -> bool:
        """Delete a key from the generic memory cache."""
        return self._memory.delete(key)

    def clear(self, *, namespace: str | None = None) -> None:
        """Clear one namespace or all managed caches."""
        if namespace is None:
            self._memory.clear()
            self._context.clear()
            self._registry.clear()
            return
        if namespace in {"memory", "default"}:
            self._memory.clear()
            return
        if namespace == "context":
            self._context.clear()
            return
        if namespace == "registry":
            self._registry.clear()
            return
        raise CacheError(f"unknown_cache_namespace:{namespace}")

    def stats(self) -> dict[str, Any]:
        """Return aggregated statistics for all managed caches."""
        context_stats = self._context.stats()
        registry_stats = self._registry.stats()
        return {
            "policy": {
                "enabled": self._policy.enabled,
                "max_entries": self._policy.max_entries,
                "ttl_seconds": self._policy.ttl_seconds,
                "eviction": self._policy.eviction.value,
                "namespace": self._policy.namespace,
            },
            "memory": self._memory.stats().to_dict(),
            "context": {
                key: value.to_dict() for key, value in context_stats.items()
            },
            "registry": {
                key: value.to_dict() for key, value in registry_stats.items()
            },
        }

    def snapshot_stats(self) -> Mapping[str, CacheStats | dict[str, CacheStats]]:
        """Return typed stats objects for diagnostics."""
        return {
            "memory": self._memory.stats(),
            "context": self._context.stats(),
            "registry": self._registry.stats(),
        }
