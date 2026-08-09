"""Rule Engine domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping


PRIORITY_LEVEL_RANK: dict[str, int] = {
    "critical": 100,
    "highest": 95,
    "high": 80,
    "medium": 50,
    "normal": 50,
    "low": 20,
    "lowest": 10,
    "info": 5,
}

KNOWN_CATEGORIES: frozenset[str] = frozenset(
    {
        "strength",
        "season",
        "temperature",
        "pattern",
        "special_case",
        "follow_pattern",
        "combination",
        "priority",
        "useful_god",
        "ten_god",
        "five_element",
        "shensha",
        "luck",
        "support",
        "element_support",
        "special",
    }
)


def _freeze_mapping(data: Mapping[str, Any] | None) -> Mapping[str, Any]:
    """Return a read-only mapping."""
    if data is None:
        return MappingProxyType({})
    return MappingProxyType(dict(data))


def _freeze_list(items: list[Any] | tuple[Any, ...] | None) -> tuple[Any, ...]:
    """Return an immutable tuple copy."""
    if not items:
        return ()
    return tuple(items)


@dataclass(frozen=True, slots=True)
class RuleRecord:
    """Immutable runtime rule record."""

    id: str
    code: str
    name: str
    category: str
    domain: str
    priority_level: str
    priority_order: int
    enabled: bool
    tags: tuple[str, ...]
    conditions: tuple[Mapping[str, Any], ...]
    condition_group: str
    source_path: str
    raw: Mapping[str, Any] = field(repr=False)

    @property
    def specificity(self) -> int:
        """Condition count used for deterministic conflict resolution."""
        return len(self.conditions)

    def to_dict(self) -> dict[str, Any]:
        """Serialize a stable public view of the rule."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category": self.category,
            "domain": self.domain,
            "priority": {
                "level": self.priority_level,
                "order": self.priority_order,
            },
            "enabled": self.enabled,
            "tags": list(self.tags),
            "conditions": [dict(item) for item in self.conditions],
            "condition_group": self.condition_group,
            "source_path": self.source_path,
        }


@dataclass(frozen=True, slots=True)
class ValidationDiagnostic:
    """Structured validation diagnostic."""

    code: str
    message: str
    severity: str
    rule_id: str | None = None
    field: str | None = None
    source_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize diagnostic."""
        return {
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "rule_id": self.rule_id,
            "field": self.field,
            "source_path": self.source_path,
        }


@dataclass(frozen=True, slots=True)
class MatchResult:
    """One matched rule with ranking metadata."""

    rule: RuleRecord
    rank: int
    matched: bool = True

    def to_dict(self) -> dict[str, Any]:
        """Serialize match result."""
        return {
            "rule_id": self.rule.id,
            "rank": self.rank,
            "matched": self.matched,
            "priority_level": self.rule.priority_level,
            "priority_order": self.rule.priority_order,
            "specificity": self.rule.specificity,
        }


@dataclass(frozen=True, slots=True)
class LoadResult:
    """Outcome of a load/reload operation."""

    loaded: int
    skipped_disabled: int
    invalid: int
    diagnostics: tuple[ValidationDiagnostic, ...]
    source_files: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize load result."""
        return {
            "loaded": self.loaded,
            "skipped_disabled": self.skipped_disabled,
            "invalid": self.invalid,
            "diagnostics": [item.to_dict() for item in self.diagnostics],
            "source_files": list(self.source_files),
        }


@dataclass(frozen=True, slots=True)
class EngineStatistics:
    """Runtime statistics for the Rule Engine."""

    loaded_rules: int
    categories: int
    tags: int
    cache_ready: bool
    source_files: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize statistics."""
        return {
            "loaded_rules": self.loaded_rules,
            "categories": self.categories,
            "tags": self.tags,
            "cache_ready": self.cache_ready,
            "source_files": self.source_files,
        }


def build_rule_record(
    raw: Mapping[str, Any],
    *,
    source_path: str,
) -> RuleRecord:
    """Build an immutable RuleRecord from a raw rule mapping."""
    classification = raw.get("classification")
    classification_map = classification if isinstance(classification, Mapping) else {}
    priority = raw.get("priority")
    priority_map = priority if isinstance(priority, Mapping) else {}
    lifecycle = raw.get("lifecycle")
    lifecycle_map = lifecycle if isinstance(lifecycle, Mapping) else {}
    metadata = raw.get("metadata")
    metadata_map = metadata if isinstance(metadata, Mapping) else {}

    tags_raw = metadata_map.get("tags") or raw.get("tags") or []
    tags = tuple(str(tag) for tag in tags_raw) if isinstance(tags_raw, (list, tuple)) else ()

    conditions_raw = raw.get("conditions") or []
    conditions: list[Mapping[str, Any]] = []
    if isinstance(conditions_raw, list):
        for item in conditions_raw:
            if isinstance(item, Mapping):
                conditions.append(_freeze_mapping(dict(item)))

    enabled = bool(lifecycle_map.get("enabled", True))
    status = str(lifecycle_map.get("status") or metadata_map.get("status") or "active").lower()
    if status in {"disabled", "inactive"}:
        enabled = False
    if bool(lifecycle_map.get("deprecated", False)) and lifecycle_map.get("enabled") is False:
        enabled = False

    category = str(
        classification_map.get("category")
        or classification_map.get("domain")
        or raw.get("category")
        or ""
    ).strip()
    domain = str(
        classification_map.get("domain")
        or raw.get("domain")
        or category
        or ""
    ).strip()

    level = str(priority_map.get("level") or raw.get("priority_level") or "medium").strip().lower()
    order_raw = priority_map.get("order", raw.get("priority_order", 0))
    try:
        order = int(order_raw)
    except (TypeError, ValueError):
        order = 0

    group = str(raw.get("condition_group") or "AND").strip().upper() or "AND"

    return RuleRecord(
        id=str(raw.get("id") or "").strip(),
        code=str(raw.get("code") or "").strip(),
        name=str(raw.get("name") or "").strip(),
        category=category,
        domain=domain,
        priority_level=level or "medium",
        priority_order=order,
        enabled=enabled,
        tags=tags,
        conditions=_freeze_list(conditions),
        condition_group=group,
        source_path=source_path,
        raw=_freeze_mapping(dict(raw)),
    )
