"""ShenShaFacts — domain truth copied from production ShenShaService, not recalculated."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.interpretation_engine.foundation.facts.shensha import (
    ShenShaInterpretationFacts,
    ShenShaItemFact,
)
from engines.interpretation_engine.foundation.knowledge.diagnostics import (
    INVALID_SHENSHA,
)
from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    INTERPRETATION_CLASS_RELATIONSHIP,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    SHEN_SHA_KEYS,
)
from engines.interpretation_engine.foundation.status import DataAvailability


@dataclass(frozen=True, slots=True)
class ShenShaMatch:
    """One copied Shen Sha match with chart context, not a new detection."""

    name: str
    pillar: str
    stem: str
    branch: str
    match_reason: str
    rule_id: str
    confidence: float
    evidence: str
    activation_context: Mapping[str, str]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one match without customer prose."""
        return {
            "name": self.name,
            "pillar": self.pillar,
            "stem": self.stem,
            "branch": self.branch,
            "match_reason": self.match_reason,
            "rule_id": self.rule_id,
            "confidence": self.confidence,
            "evidence": self.evidence,
            "activation_context": dict(self.activation_context),
        }


@dataclass(frozen=True, slots=True)
class ShenShaFacts:
    """Structured Shen Sha domain facts for relationship + knowledge."""

    matched_shensha: tuple[str, ...]
    matches: tuple[ShenShaMatch, ...]
    related_stems: tuple[str, ...]
    related_branches: tuple[str, ...]
    related_pillars: tuple[str, ...]
    day_master: str
    pattern_label: str
    ten_god_roles: tuple[str, ...]
    strength_context: str
    status: DataAvailability
    interpretation_class: str = INTERPRETATION_CLASS_RELATIONSHIP
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize Shen Sha facts without customer prose."""
        return {
            "matched_shensha": list(self.matched_shensha),
            "matches": [item.to_dict() for item in self.matches],
            "related_stems": list(self.related_stems),
            "related_branches": list(self.related_branches),
            "related_pillars": list(self.related_pillars),
            "day_master": self.day_master,
            "pattern_label": self.pattern_label,
            "ten_god_roles": list(self.ten_god_roles),
            "strength_context": self.strength_context,
            "status": self.status.value,
            "interpretation_class": self.interpretation_class,
            "diagnostics": list(self.diagnostics),
        }


def build_shensha_facts(
    facts: ShenShaInterpretationFacts,
    *,
    matched_names: tuple[str, ...] | list[str] = (),
    day_master: str = "",
    stems: tuple[str, ...] | list[str] = (),
    branches: tuple[str, ...] | list[str] = (),
    pillars: Mapping[str, str] | None = None,
    pattern_label: str = "",
    ten_god_roles: tuple[str, ...] | list[str] = (),
    strength_level: str = "",
) -> ShenShaFacts:
    """Copy existing production Shen Sha names into ShenShaFacts. Do not rematch."""
    pillar_map = dict(pillars or {})
    names = _unique([*(item.name for item in facts.items), *matched_names])
    context = {
        "day_master": str(day_master or ""),
        "pattern_label": str(pattern_label or ""),
        "strength": str(strength_level or ""),
    }
    by_name = {item.name: item for item in facts.items if item.name}
    matches = tuple(
        _copy_match(by_name.get(name), name, context) for name in names
    )
    diagnostics = tuple(
        dict.fromkeys(INVALID_SHENSHA for name in names if name not in SHEN_SHA_KEYS)
    )
    related_pillars = tuple(
        f"{slot}:{value}" for slot, value in pillar_map.items() if value
    )
    return ShenShaFacts(
        matched_shensha=names,
        matches=matches,
        related_stems=_unique(stems),
        related_branches=_unique(branches),
        related_pillars=related_pillars,
        day_master=str(day_master or ""),
        pattern_label=str(pattern_label or ""),
        ten_god_roles=_unique(ten_god_roles),
        strength_context=str(strength_level or ""),
        status=DataAvailability.AVAILABLE if names else facts.status,
        diagnostics=diagnostics,
    )


def _copy_match(
    item: ShenShaItemFact | None,
    name: str,
    context: Mapping[str, str],
) -> ShenShaMatch:
    """Copy one foundation item, or presence of a production name, into a match."""
    if item is None:
        return ShenShaMatch(
            name=name,
            pillar="",
            stem="",
            branch="",
            match_reason="PRESENT",
            rule_id="",
            confidence=1.0,
            evidence=f"present:{name}",
            activation_context=dict(context),
        )
    evidence = str(item.evidence or f"present:{item.name}")
    reason = str(item.matched_condition or "PRESENT")
    return ShenShaMatch(
        name=item.name,
        pillar=str(item.position or ""),
        stem="",
        branch="",
        match_reason=reason,
        rule_id=str(item.rule_id or ""),
        confidence=1.0,
        evidence=evidence,
        activation_context=dict(context),
    )


def _unique(values: Any) -> tuple[str, ...]:
    """Drop empty duplicates, keep order."""
    return tuple(dict.fromkeys(str(item) for item in values if str(item).strip()))
