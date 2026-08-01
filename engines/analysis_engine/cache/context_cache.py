"""Context cache for in-memory Analysis Context artifacts."""

from __future__ import annotations

from engines.analysis_engine.cache.cache_policy import CachePolicy
from engines.analysis_engine.cache.memory_cache import CacheStats, MemoryCache
from engines.analysis_engine.context.context_snapshot import ContextSnapshot
from engines.analysis_engine.models.analysis_context import AnalysisContext


class ContextCache:
    """Memory-only cache for Analysis Context and context snapshots.

    Does not persist to external stores and does not run analyzer logic.
    """

    def __init__(self, policy: CachePolicy | None = None) -> None:
        """Initialize context cache with an optional policy."""
        resolved = policy or CachePolicy(namespace="context")
        if resolved.namespace == "default":
            resolved = CachePolicy(
                enabled=resolved.enabled,
                max_entries=resolved.max_entries,
                ttl_seconds=resolved.ttl_seconds,
                eviction=resolved.eviction,
                namespace="context",
            )
        self._contexts = MemoryCache(resolved)
        snapshot_policy = CachePolicy(
            enabled=resolved.enabled,
            max_entries=resolved.max_entries,
            ttl_seconds=resolved.ttl_seconds,
            eviction=resolved.eviction,
            namespace="context_snapshot",
        )
        self._snapshots = MemoryCache(snapshot_policy)

    def get_context(self, context_id: str) -> AnalysisContext | None:
        """Return a cached Analysis Context by identifier."""
        value = self._contexts.get(context_id)
        return value if isinstance(value, AnalysisContext) else None

    def put_context(self, context: AnalysisContext) -> None:
        """Store an Analysis Context in memory."""
        self._contexts.set(context.id, context)

    def invalidate_context(self, context_id: str) -> bool:
        """Invalidate a cached context by identifier."""
        return self._contexts.delete(context_id)

    def get_snapshot(self, snapshot_id: str) -> ContextSnapshot | None:
        """Return a cached context snapshot by identifier."""
        value = self._snapshots.get(snapshot_id)
        return value if isinstance(value, ContextSnapshot) else None

    def put_snapshot(self, snapshot: ContextSnapshot) -> None:
        """Store a context snapshot in memory."""
        self._snapshots.set(snapshot.snapshot_id, snapshot)

    def invalidate_snapshot(self, snapshot_id: str) -> bool:
        """Invalidate a cached context snapshot by identifier."""
        return self._snapshots.delete(snapshot_id)

    def clear(self) -> None:
        """Clear all cached context artifacts."""
        self._contexts.clear()
        self._snapshots.clear()

    def stats(self) -> dict[str, CacheStats]:
        """Return stats for context and snapshot stores."""
        return {
            "contexts": self._contexts.stats(),
            "snapshots": self._snapshots.stats(),
        }
