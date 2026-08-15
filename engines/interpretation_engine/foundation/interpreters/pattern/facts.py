"""PatternFacts — domain truth copied from Pattern Engine, not recalculated."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.facts.pattern import (
    PatternInterpretationFacts,
)
from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    INTERPRETATION_CLASS_RELATIONSHIP,
)
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class PatternFacts:
    """Structured Pattern domain facts for relationship + knowledge.

    Copies PatternInterpretationFacts and optional PatternResult / PatternContext
    fields. Does not rerun Pattern Engine.
    """

    selected: str
    label: str
    candidate_patterns: tuple[str, ...]
    month_command: str
    supporting_relationships: tuple[str, ...]
    rule_ids: tuple[str, ...]
    confidence: float
    reason: str
    related_pillars: tuple[str, ...]
    day_master: str
    ten_gods: tuple[str, ...]
    status: DataAvailability
    interpretation_class: str = INTERPRETATION_CLASS_RELATIONSHIP
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize pattern facts without customer prose."""
        return {
            "selected": self.selected,
            "label": self.label,
            "candidate_patterns": list(self.candidate_patterns),
            "month_command": self.month_command,
            "supporting_relationships": list(self.supporting_relationships),
            "rule_ids": list(self.rule_ids),
            "confidence": self.confidence,
            "reason": self.reason,
            "related_pillars": list(self.related_pillars),
            "day_master": self.day_master,
            "ten_gods": list(self.ten_gods),
            "status": self.status.value,
            "interpretation_class": self.interpretation_class,
            "diagnostics": list(self.diagnostics),
        }


def build_pattern_facts(
    facts: PatternInterpretationFacts,
    *,
    pattern_context: Any | None = None,
    pattern_result: Any | None = None,
) -> PatternFacts:
    """Copy existing engine truth into PatternFacts. Do not recalculate."""
    selected = str(getattr(pattern_result, "pattern", None) or facts.selected or "")
    label = str(
        getattr(pattern_result, "cach_cuc", None) or facts.label or selected
    )
    candidates = _tuple(getattr(pattern_result, "candidate_patterns", None))
    rule_ids = _tuple(getattr(pattern_result, "matched_rules", None)) or facts.rule_ids
    reason = str(
        getattr(pattern_result, "reason", None)
        or getattr(pattern_result, "description", None)
        or (facts.evidence[0] if facts.evidence else "")
    )
    confidence = _confidence(facts, pattern_result)
    month_command = str(getattr(pattern_context, "month_branch_ten_god", None) or "")
    day_master = str(getattr(pattern_context, "day_master", None) or "")
    ten_gods = _tuple(getattr(pattern_context, "ten_gods_list", None))
    supporting = _unique((month_command, *ten_gods))
    related_pillars = _pillars(pattern_context)
    diagnostics = list(facts.diagnostics)
    return PatternFacts(
        selected=selected,
        label=label,
        candidate_patterns=candidates,
        month_command=month_command,
        supporting_relationships=supporting,
        rule_ids=rule_ids,
        confidence=confidence,
        reason=reason,
        related_pillars=related_pillars,
        day_master=day_master,
        ten_gods=ten_gods,
        status=facts.status,
        diagnostics=tuple(diagnostics),
    )


def _confidence(facts: PatternInterpretationFacts, pattern_result: Any | None) -> float:
    """Prefer PatternResult.confidence (0–1); never rescale scores."""
    if pattern_result is not None:
        return float(getattr(pattern_result, "confidence", 0.0) or 0.0)
    value = float(facts.confidence or 0.0)
    if 0.0 <= value <= 1.0:
        return value
    return 0.0


def _pillars(pattern_context: Any | None) -> tuple[str, ...]:
    """Copy pillar strings already present on PatternContext."""
    if pattern_context is None:
        return ()
    items: list[str] = []
    for name in ("year_pillar", "month_pillar", "day_pillar", "hour_pillar"):
        value = str(getattr(pattern_context, name, None) or "").strip()
        if value:
            slot = name[:-7] if name.endswith("_pillar") else name
            items.append(f"{slot}:{value}")
    return tuple(items)


def _tuple(value: Any) -> tuple[str, ...]:
    """Preserve order while dropping empties."""
    if not value:
        return ()
    return tuple(dict.fromkeys(str(item) for item in value if str(item).strip()))


def _unique(values: tuple[str, ...]) -> tuple[str, ...]:
    """Drop empty duplicates, keep order."""
    return tuple(dict.fromkeys(item for item in values if item))
