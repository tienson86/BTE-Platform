"""Support synthesis for the primary pattern."""

from __future__ import annotations

from engines.mingju.constants import FAMILY_CONTROLS, FAMILY_GENERATES, GOD_FAMILY
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power
from engines.mingju.models import MingJuContext, PatternDecision, SupportResult
from engines.mingju.serialization import clamp_confidence, clamp_score


def evaluate_support(
    context: MingJuContext,
    pattern: PatternDecision,
    book: RecordBook,
) -> SupportResult:
    """Measure generating and controlling support around the pattern family."""
    if pattern.state != AnalysisState.RESOLVED.value:
        return SupportResult(state=AnalysisState.UNRESOLVED.value, classification="unresolved")
    family = GOD_FAMILY.get(pattern.pattern_id, "")
    generating = next((source for source, target in FAMILY_GENERATES.items() if target == family), "")
    controlling = next((source for source, target in FAMILY_CONTROLS.items() if target == family), "")
    generating_support = family_power(context.activations, generating) if generating else 0.0
    controlling_support = family_power(context.activations, controlling) if controlling else 0.0
    score = clamp_score(40.0 + generating_support * 12.0 + controlling_support * 6.0)
    evidence_id = book.add_evidence(
        "support",
        "mc01.support.families",
        source="mingju.support",
        generating_family=generating,
        controlling_family=controlling,
        generating_support=generating_support,
        controlling_support=controlling_support,
    )
    classification = "strong" if score >= 70 else "moderate" if score >= 45 else "weak"
    book.add_trace("support", "MC-SUP-000", "mc01.support.resolved", (evidence_id,))
    return SupportResult(
        state=AnalysisState.RESOLVED.value,
        classification=classification,
        score=score,
        generating_support=round(generating_support, 4),
        controlling_support=round(controlling_support, 4),
        evidence_ids=(evidence_id,),
        confidence=clamp_confidence(0.8 if context.hour_present else 0.62),
    )
