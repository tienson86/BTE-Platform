"""In-memory immutable rule cache."""

from __future__ import annotations

from threading import RLock

from engines.rule_engine.models import LoadResult, RuleRecord


class RuleCache:
    """Thread-safe in-memory cache for loaded rules."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._rules: tuple[RuleRecord, ...] | None = None
        self._load_result: LoadResult | None = None
        self._root: str | None = None

    @property
    def ready(self) -> bool:
        """Whether the cache has been initialized."""
        with self._lock:
            return self._rules is not None

    def get_rules(self) -> tuple[RuleRecord, ...] | None:
        """Return cached immutable rules, or None when uninitialized."""
        with self._lock:
            return self._rules

    def get_load_result(self) -> LoadResult | None:
        """Return cached load diagnostics."""
        with self._lock:
            return self._load_result

    def get_root(self) -> str | None:
        """Return cached rules root path."""
        with self._lock:
            return self._root

    def store(
        self,
        rules: list[RuleRecord] | tuple[RuleRecord, ...],
        *,
        load_result: LoadResult,
        root: str,
    ) -> None:
        """Replace cache contents with an immutable snapshot."""
        with self._lock:
            self._rules = tuple(rules)
            self._load_result = load_result
            self._root = root

    def invalidate(self) -> None:
        """Cache invalidation entry point."""
        with self._lock:
            self._rules = None
            self._load_result = None
            self._root = None
