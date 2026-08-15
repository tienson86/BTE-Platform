"""State assessment models — Strength is assessment, not decision."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from engines.interpretation_engine.foundation.facts.strength import (
    StrengthInterpretationFacts,
)
from engines.interpretation_engine.foundation.knowledge.domain_classes import (
    INTERPRETATION_CLASS_STATE,
)
from engines.interpretation_engine.foundation.knowledge.entity_types import (
    STRENGTH_STATE_KEYS,
)
from engines.interpretation_engine.foundation.ownership import DOMAIN_OWNERS

STRENGTH_ASSESSMENT_PATH: tuple[str, ...] = (
    "season",
    "roots",
    "support",
    "drain",
    "control",
    "balance",
    "strength",
)

_STEP_TITLES: dict[str, str] = {
    "season": "Season",
    "roots": "Roots",
    "support": "Support",
    "drain": "Drain",
    "control": "Control",
    "balance": "Balance",
    "strength": "Strength",
}

_STRENGTH_DOMAIN = "Strength"
_OWNER = DOMAIN_OWNERS["strength"]


@dataclass(frozen=True, slots=True)
class AssessmentPathStep:
    """One step on a state assessment path — no winner, no alternatives."""

    step_id: str
    order: int
    title: str
    value: str
    source: str
    status: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize assessment path step."""
        return {
            "step_id": self.step_id,
            "order": self.order,
            "title": self.title,
            "value": self.value,
            "source": self.source,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class StrengthAssessment:
    """Canonical Strength assessment built from existing engine facts.

    Reuses StrengthInterpretationFacts and optional StrengthResult component
    scores. Does not recalculate strength, does not select a winner, and
    does not generate narrative.
    """

    state: str
    confidence: float
    assessment_path: tuple[AssessmentPathStep, ...]
    evidence: tuple[str, ...]
    support: float
    drain: float
    control: float
    season: float
    roots: float
    balance: float
    label: str = ""
    score: float = 0.0
    rule_ids: tuple[str, ...] = ()
    domain: str = _STRENGTH_DOMAIN
    interpretation_class: str = INTERPRETATION_CLASS_STATE
    diagnostics: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize assessment without generating customer prose."""
        return {
            "domain": self.domain,
            "interpretation_class": self.interpretation_class,
            "state": self.state,
            "label": self.label,
            "score": self.score,
            "confidence": self.confidence,
            "assessment_path": [item.to_dict() for item in self.assessment_path],
            "evidence": list(self.evidence),
            "support": self.support,
            "drain": self.drain,
            "control": self.control,
            "season": self.season,
            "roots": self.roots,
            "balance": self.balance,
            "rule_ids": list(self.rule_ids),
            "diagnostics": list(self.diagnostics),
        }


def build_strength_assessment(
    facts: StrengthInterpretationFacts,
    *,
    strength_result: Any | None = None,
) -> StrengthAssessment:
    """Build StrengthAssessment from canonical facts; do not recalculate.

    Component scores are copied from an existing StrengthResult when provided.
    Missing component scores are left at 0.0 with skipped path steps.
    """
    state = str(facts.level or "").strip()
    season = _component(strength_result, "season_score")
    roots = _component(strength_result, "root_score")
    support = _component(strength_result, "support_score")
    drain = _component(strength_result, "drain_score")
    control = _component(strength_result, "control_score")
    balance = float(facts.score)
    components_present = strength_result is not None
    path = _build_path(
        state=state,
        season=season,
        roots=roots,
        support=support,
        drain=drain,
        control=control,
        balance=balance,
        components_present=components_present,
    )
    diagnostics: list[str] = list(facts.diagnostics)
    if state and state not in STRENGTH_STATE_KEYS:
        diagnostics.append("invalid_strength_state")
    return StrengthAssessment(
        state=state,
        confidence=float(facts.confidence),
        assessment_path=path,
        evidence=tuple(facts.evidence),
        support=support,
        drain=drain,
        control=control,
        season=season,
        roots=roots,
        balance=balance,
        label=str(facts.label or ""),
        score=float(facts.score),
        rule_ids=tuple(facts.rule_ids),
        diagnostics=tuple(dict.fromkeys(diagnostics)),
    )


def _component(result: Any | None, attr: str) -> float:
    """Copy one existing component score; never recompute."""
    if result is None:
        return 0.0
    return float(getattr(result, attr, 0.0) or 0.0)


def _build_path(
    *,
    state: str,
    season: float,
    roots: float,
    support: float,
    drain: float,
    control: float,
    balance: float,
    components_present: bool,
) -> tuple[AssessmentPathStep, ...]:
    """Season → Roots → Support → Drain → Control → Balance → Strength."""
    scores = {
        "season": season,
        "roots": roots,
        "support": support,
        "drain": drain,
        "control": control,
        "balance": balance,
    }
    steps: list[AssessmentPathStep] = []
    for order, step_id in enumerate(STRENGTH_ASSESSMENT_PATH, start=1):
        if step_id == "strength":
            value = state
            status = "passed" if state else "skipped"
        elif step_id == "balance":
            value = str(balance)
            status = "passed"
        else:
            value = str(scores[step_id]) if components_present else ""
            status = "passed" if components_present else "skipped"
        steps.append(
            AssessmentPathStep(
                step_id=step_id,
                order=order,
                title=_STEP_TITLES[step_id],
                value=value,
                source=_OWNER,
                status=status,
            )
        )
    return tuple(steps)
