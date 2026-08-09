"""Centralized runtime rule registry."""

from __future__ import annotations

from threading import RLock

from engines.rule_engine.models import RuleRecord


class RuleRegistry:
    """Canonical in-memory index of loaded rules."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._by_id: dict[str, RuleRecord] = {}
        self._by_category: dict[str, list[str]] = {}
        self._by_tag: dict[str, list[str]] = {}
        self._by_priority: dict[str, list[str]] = {}
        self._order: list[str] = []

    def clear(self) -> None:
        """Remove all registered rules."""
        with self._lock:
            self._by_id.clear()
            self._by_category.clear()
            self._by_tag.clear()
            self._by_priority.clear()
            self._order.clear()

    def register(self, rule: RuleRecord) -> None:
        """Register one rule into the runtime index."""
        with self._lock:
            existing = self._by_id.get(rule.id)
            if existing is not None:
                self._remove_indexes(existing)
                if rule.id in self._order:
                    self._order.remove(rule.id)
            self._by_id[rule.id] = rule
            self._order.append(rule.id)
            self._index(rule)

    def register_many(self, rules: list[RuleRecord]) -> None:
        """Register many rules in order."""
        for rule in rules:
            self.register(rule)

    def unregister(self, rule_id: str) -> bool:
        """Unregister a rule by id. Returns True when removed."""
        with self._lock:
            rule = self._by_id.pop(rule_id, None)
            if rule is None:
                return False
            self._remove_indexes(rule)
            if rule_id in self._order:
                self._order.remove(rule_id)
            return True

    def get(self, rule_id: str) -> RuleRecord | None:
        """Search by id."""
        with self._lock:
            return self._by_id.get(rule_id)

    def search_by_id(self, rule_id: str) -> RuleRecord | None:
        """Alias for get()."""
        return self.get(rule_id)

    def search_by_category(self, category: str) -> list[RuleRecord]:
        """Search by category."""
        key = category.strip().lower()
        with self._lock:
            ids = list(self._by_category.get(key, []))
            return [self._by_id[item] for item in ids if item in self._by_id]

    def search_by_priority(self, priority_level: str) -> list[RuleRecord]:
        """Search by priority level."""
        key = priority_level.strip().lower()
        with self._lock:
            ids = list(self._by_priority.get(key, []))
            return [self._by_id[item] for item in ids if item in self._by_id]

    def search_by_tag(self, tag: str) -> list[RuleRecord]:
        """Search by tag."""
        key = tag.strip().lower()
        with self._lock:
            ids = list(self._by_tag.get(key, []))
            return [self._by_id[item] for item in ids if item in self._by_id]

    def all_rules(self) -> list[RuleRecord]:
        """Enumerate all loaded rules in registration order."""
        with self._lock:
            return [self._by_id[item] for item in self._order if item in self._by_id]

    def count(self) -> int:
        """Return number of registered rules."""
        with self._lock:
            return len(self._by_id)

    def categories(self) -> list[str]:
        """Return sorted category keys."""
        with self._lock:
            return sorted(self._by_category)

    def tags(self) -> list[str]:
        """Return sorted tag keys."""
        with self._lock:
            return sorted(self._by_tag)

    def _index(self, rule: RuleRecord) -> None:
        """Add secondary indexes for one rule."""
        category = rule.category.strip().lower()
        if category:
            self._by_category.setdefault(category, []).append(rule.id)
        level = rule.priority_level.strip().lower()
        if level:
            self._by_priority.setdefault(level, []).append(rule.id)
        for tag in rule.tags:
            key = str(tag).strip().lower()
            if key:
                self._by_tag.setdefault(key, []).append(rule.id)

    def _remove_indexes(self, rule: RuleRecord) -> None:
        """Remove secondary indexes for one rule."""
        category = rule.category.strip().lower()
        if category and category in self._by_category:
            self._by_category[category] = [
                item for item in self._by_category[category] if item != rule.id
            ]
            if not self._by_category[category]:
                del self._by_category[category]
        level = rule.priority_level.strip().lower()
        if level and level in self._by_priority:
            self._by_priority[level] = [
                item for item in self._by_priority[level] if item != rule.id
            ]
            if not self._by_priority[level]:
                del self._by_priority[level]
        for tag in rule.tags:
            key = str(tag).strip().lower()
            if key and key in self._by_tag:
                self._by_tag[key] = [item for item in self._by_tag[key] if item != rule.id]
                if not self._by_tag[key]:
                    del self._by_tag[key]
