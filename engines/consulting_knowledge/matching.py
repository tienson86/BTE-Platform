"""Match published signals to consulting knowledge units. No calculation."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from engines.consulting_knowledge.models import (
    ConsultingKnowledgePack,
    ConsultingKnowledgeUnit,
    empty_knowledge_pack,
)


def project_signals(
    *,
    integrated_narrative: Mapping[str, Any] | None = None,
    identity: Mapping[str, Any] | None = None,
    analysis_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Copy published inputs into a flat signal map. Do not compute new fields."""
    signals: dict[str, Any] = {}
    if isinstance(analysis_result, Mapping):
        signals.update(_flatten("analysis", analysis_result))
    if isinstance(identity, Mapping):
        signals.update(_flatten("identity", identity))
    if isinstance(integrated_narrative, Mapping):
        signals.update(_flatten("integrated", integrated_narrative))
    return signals


def match_consulting_knowledge(
    signals: Mapping[str, Any] | None = None,
    catalog: Sequence[ConsultingKnowledgeUnit] | None = None,
) -> ConsultingKnowledgePack:
    """Return catalog units whose conditions match published signals."""
    if not catalog:
        return empty_knowledge_pack()
    published = dict(signals or {})
    matched: list[ConsultingKnowledgeUnit] = []
    refs: list[str] = []
    for unit in catalog:
        if not _condition_matches(unit.condition, published):
            continue
        if not _scope_allows(unit.applicable_scope, published):
            continue
        matched.append(unit)
        refs.extend(unit.references)
    if not matched:
        return empty_knowledge_pack()
    complete = all(unit.status == "complete" for unit in matched)
    return ConsultingKnowledgePack(
        units=tuple(matched),
        status="complete" if complete else "partial",
        evidence_refs=tuple(refs),
    )


def _flatten(prefix: str, payload: Mapping[str, Any], *, depth: int = 0) -> dict[str, Any]:
    """Copy nested published scalars into dotted keys."""
    flat: dict[str, Any] = {}
    if depth > 3:
        return flat
    for key, value in payload.items():
        path = f"{prefix}.{key}"
        if isinstance(value, Mapping):
            flat.update(_flatten(path, value, depth=depth + 1))
        elif isinstance(value, (str, int, float, bool)):
            flat[path] = value
            flat[str(key)] = value
        elif isinstance(value, (list, tuple)) and all(isinstance(item, str) for item in value):
            flat[path] = tuple(value)
            flat[str(key)] = tuple(value)
    return flat


def _condition_matches(condition: Mapping[str, Any], signals: Mapping[str, Any]) -> bool:
    """True when every condition key is present and equal or a member."""
    if not condition:
        return False
    for key, expected in condition.items():
        actual = signals.get(key)
        if actual is None:
            return False
        if isinstance(expected, (list, tuple)):
            if actual not in expected and not (
                isinstance(actual, (list, tuple)) and set(expected).issubset(actual)
            ):
                return False
            continue
        if isinstance(actual, (list, tuple)):
            if expected not in actual:
                return False
            continue
        if actual != expected:
            return False
    return True


def _scope_allows(scope: Mapping[str, Any], signals: Mapping[str, Any]) -> bool:
    """True when optional scope keys are absent or match published signals."""
    domain = scope.get("domain")
    if domain is not None and "domain" in signals and signals["domain"] != domain:
        return False
    audience = scope.get("audience")
    if audience is not None and "audience" in signals and signals["audience"] != audience:
        return False
    return True
