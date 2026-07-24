"""
Rule Contract V1 models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping, Sequence


# Operators required by WP2B-2 (+ aliases from contract doc)
OPERATORS_V1: frozenset[str] = frozenset(
    {
        "eq",
        "neq",
        "gt",
        "gte",
        "lt",
        "lte",
        "in",
        "not_in",
        "contains",
        "contains_any",
        "contains_all",
        "exists",
        "not_exists",
        "between",
    }
)

OPERATOR_ALIASES: dict[str, str] = {
    "==": "eq",
    "=": "eq",
    "!=": "neq",
    ">": "gt",
    ">=": "gte",
    "<": "lt",
    "<=": "lte",
    "eq": "eq",
    "neq": "neq",
    "gt": "gt",
    "gte": "gte",
    "lt": "lt",
    "lte": "lte",
    "in": "in",
    "not_in": "not_in",
    "contains": "contains",
    "contains_any": "contains_any",
    "contains_all": "contains_all",
    "exists": "exists",
    "not_exists": "not_exists",
    "between": "between",
}


@dataclass(slots=True)
class ConditionPredicate:
    """One V1 predicate: field + operator + value."""

    condition_id: str
    field: str
    operator: str
    value: Any = None

    def normalized_operator(self) -> str:
        """Return canonical operator name."""
        op = str(self.operator).strip().lower()
        return OPERATOR_ALIASES.get(op, op)

    def to_dict(self) -> dict[str, Any]:
        """Serialize predicate."""
        return {
            "condition_id": self.condition_id,
            "field": self.field,
            "operator": self.normalized_operator(),
            "value": self.value,
        }


@dataclass(slots=True)
class RuleContract:
    """Rule Contract V1 envelope."""

    condition_group: str = "AND"
    conditions: list[ConditionPredicate] = field(default_factory=list)
    source_type: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_unconditional(self) -> bool:
        """Empty conditions list means always true."""
        return len(self.conditions) == 0

    def to_dict(self) -> dict[str, Any]:
        """Serialize contract."""
        return {
            "condition_group": self.condition_group.upper(),
            "conditions": [item.to_dict() for item in self.conditions],
            "source_type": self.source_type,
            "metadata": dict(self.metadata),
        }


# RuleContext is a plain mutable mapping (dict-compatible)
RuleContext = MutableMapping[str, Any]


def normalize_context(context: Any) -> dict[str, Any]:
    """
    Normalize engine context objects into a plain RuleContext dict.

    Supports:
    - dict / Mapping
    - objects with ``to_dict``
    - dataclasses / simple objects via ``__dict__`` / ``vars``
    """
    if context is None:
        return {}

    if isinstance(context, dict):
        return dict(context)

    if isinstance(context, Mapping):
        return dict(context)

    to_dict = getattr(context, "to_dict", None)
    if callable(to_dict):
        data = to_dict()
        if isinstance(data, dict):
            return dict(data)

    if hasattr(context, "__dict__"):
        raw = {
            key: value
            for key, value in vars(context).items()
            if not key.startswith("_")
        }
        # Nested known containers
        nested: dict[str, Any] = {}
        for key, value in raw.items():
            if hasattr(value, "__dict__") and not isinstance(
                value, (str, bytes, int, float, bool, list, dict, tuple, set)
            ):
                nested[key] = normalize_context(value)
            else:
                nested[key] = value
        return nested

    return {"value": context}


def resolve_path(context: Mapping[str, Any], path: str, default: Any = None) -> Any:
    """
    Resolve dotted path against RuleContext.

    Supports ``facts`` set/list membership when path is ``facts.<name>``.
    """
    if not path:
        return default

    parts = path.split(".")
    current: Any = context

    # facts.X as boolean membership
    if len(parts) == 2 and parts[0] == "facts":
        facts = context.get("facts")
        if isinstance(facts, Mapping):
            return facts.get(parts[1], default)
        if isinstance(facts, (set, list, tuple)):
            return parts[1] in facts
        return default

    for part in parts:
        if isinstance(current, Mapping):
            if part not in current:
                return default
            current = current[part]
        else:
            current = getattr(current, part, default)
            if current is default:
                return default
    return current
