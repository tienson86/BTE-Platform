"""Canonical Rule Engine public entry point."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Mapping

from engines.rule_engine.cache import RuleCache
from engines.rule_engine.exceptions import RuleEngineError, RuleLoadError
from engines.rule_engine.loader import RuleLoader
from engines.rule_engine.matcher import RuleMatcher
from engines.rule_engine.models import (
    EngineStatistics,
    LoadResult,
    MatchResult,
    RuleRecord,
    ValidationDiagnostic,
)
from engines.rule_engine.priority import PriorityResolver
from engines.rule_engine.registry import RuleRegistry
from engines.rule_engine.validator import RuleValidator

logger = logging.getLogger(__name__)


class RuleEngine:
    """
    Canonical Rule Engine facade.

    Responsibilities: load, validate, register, match, prioritize, cache.
    No analytical knowledge and no mutation of rule data files.
    """

    def __init__(
        self,
        rules_root: Path | str | None = None,
        *,
        loader: RuleLoader | None = None,
        registry: RuleRegistry | None = None,
        matcher: RuleMatcher | None = None,
        cache: RuleCache | None = None,
        validator: RuleValidator | None = None,
        priority_resolver: PriorityResolver | None = None,
    ) -> None:
        self._rules_root = Path(rules_root) if rules_root is not None else None
        self._validator = validator or RuleValidator()
        self._loader = loader or RuleLoader(validator=self._validator)
        self._registry = registry or RuleRegistry()
        self._priority_resolver = priority_resolver or PriorityResolver()
        self._matcher = matcher or RuleMatcher(priority_resolver=self._priority_resolver)
        self._cache = cache or RuleCache()
        self._last_load: LoadResult | None = None

    @property
    def registry(self) -> RuleRegistry:
        """Expose the canonical runtime registry."""
        return self._registry

    @property
    def cache(self) -> RuleCache:
        """Expose the in-memory rule cache."""
        return self._cache

    def load(self, rules_root: Path | str | None = None) -> LoadResult:
        """Load rules from disk into registry and cache."""
        root = self._resolve_root(rules_root)
        records, result = self._loader.load(root)
        self._registry.clear()
        self._registry.register_many(records)
        self._cache.store(records, load_result=result, root=str(root))
        self._last_load = result
        self._rules_root = root
        return result

    def reload(self, rules_root: Path | str | None = None) -> LoadResult:
        """Invalidate cache and reload rules."""
        self._cache.invalidate()
        return self.load(rules_root)

    def match(
        self,
        context: Mapping[str, Any] | Any,
        *,
        category: str | None = None,
        tag: str | None = None,
        resolve_priority: bool = True,
    ) -> list[MatchResult]:
        """
        Match registered rules against context.

        Lazily initializes from cache/root when rules are not yet loaded.
        """
        rules = self._ensure_rules()
        if category is not None:
            allowed = {item.id for item in self._registry.search_by_category(category)}
            rules = [rule for rule in rules if rule.id in allowed]
        if tag is not None:
            allowed = {item.id for item in self._registry.search_by_tag(tag)}
            rules = [rule for rule in rules if rule.id in allowed]
        return self._matcher.match(
            rules,
            context,
            resolve_priority=resolve_priority,
        )

    def validate(
        self,
        rules_root: Path | str | None = None,
    ) -> list[ValidationDiagnostic]:
        """
        Validate rules under root and return structured diagnostics.

        Does not mutate the registry. Uses loader validation path.
        """
        root = self._resolve_root(rules_root)
        _records, result = self._loader.load(root)
        return list(result.diagnostics)

    def statistics(self) -> EngineStatistics:
        """Return runtime statistics for loaded rules."""
        self._ensure_rules()
        cached = self._cache.get_load_result()
        source_files = len(cached.source_files) if cached is not None else 0
        return EngineStatistics(
            loaded_rules=self._registry.count(),
            categories=len(self._registry.categories()),
            tags=len(self._registry.tags()),
            cache_ready=self._cache.ready,
            source_files=source_files,
        )

    def get_rule(self, rule_id: str) -> RuleRecord | None:
        """Lookup one rule by id."""
        self._ensure_rules()
        return self._registry.search_by_id(rule_id)

    def invalidate_cache(self) -> None:
        """Public cache invalidation entry point."""
        self._cache.invalidate()

    def _ensure_rules(self) -> list[RuleRecord]:
        """Lazy-initialize rules from cache or disk."""
        cached = self._cache.get_rules()
        if cached is not None:
            if self._registry.count() == 0 and cached:
                self._registry.register_many(list(cached))
            return list(cached)
        if self._registry.count() > 0:
            return self._registry.all_rules()
        if self._rules_root is None:
            raise RuleEngineError(
                "RuleEngine has no rules loaded. Call load(rules_root) first."
            )
        self.load(self._rules_root)
        rules = self._cache.get_rules() or ()
        return list(rules)

    def _resolve_root(self, rules_root: Path | str | None) -> Path:
        """Resolve the rules root path."""
        if rules_root is not None:
            return Path(rules_root)
        if self._rules_root is not None:
            return self._rules_root
        raise RuleLoadError("rules_root is required for load/validate.")
