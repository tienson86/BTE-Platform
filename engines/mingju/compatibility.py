"""Useful God and climate compatibility with the natal pattern."""

from __future__ import annotations

from engines.mingju.constants import GOD_FAMILY
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import normalize_god_id
from engines.mingju.models import CompatibilityResult, MingJuContext, PatternDecision
from engines.mingju.serialization import clamp_confidence, clamp_score


def evaluate_useful_god_compatibility(
    context: MingJuContext,
    pattern: PatternDecision,
    book: RecordBook,
) -> CompatibilityResult:
    """Consume Useful God Engine identity. Do not recalculate Dụng Thần."""
    if pattern.state != AnalysisState.RESOLVED.value:
        return CompatibilityResult(state=AnalysisState.UNRESOLVED.value, classification="unresolved")
    useful_id = normalize_god_id(context.useful_ten_god, context.useful_god)
    if not context.useful_god and not useful_id:
        return CompatibilityResult(
            state=AnalysisState.INSUFFICIENT_EVIDENCE.value,
            classification="unresolved",
            confidence=0.0,
        )
    aligned = useful_id == pattern.pattern_id or GOD_FAMILY.get(useful_id, "") == GOD_FAMILY.get(
        pattern.pattern_id, ""
    )
    score = 78.0 if aligned else 58.0
    if context.useful_element and context.useful_god:
        score += 6.0
    score = clamp_score(score)
    evidence_id = book.add_evidence(
        "useful_god_compatibility",
        "mc01.ug.consumed",
        source="canonical_useful_god_engine",
        useful_god=context.useful_god,
        useful_ten_god=context.useful_ten_god,
        aligned=aligned,
    )
    classification = "supportive" if score >= 70 else "mixed" if score >= 50 else "conflicting"
    return CompatibilityResult(
        state=AnalysisState.RESOLVED.value,
        classification=classification,
        score=score,
        evidence_ids=(evidence_id,),
        confidence=clamp_confidence(0.82),
    )


def evaluate_climate_compatibility(
    context: MingJuContext,
    pattern: PatternDecision,
    book: RecordBook,
) -> CompatibilityResult:
    """Consume Temperature Engine climate. Do not recalculate Điều Hậu."""
    if pattern.state != AnalysisState.RESOLVED.value:
        return CompatibilityResult(state=AnalysisState.UNRESOLVED.value, classification="unresolved")
    climate = context.climate_state.lower()
    if not climate:
        return CompatibilityResult(
            state=AnalysisState.INSUFFICIENT_EVIDENCE.value,
            classification="unresolved",
            confidence=0.0,
        )
    score = 64.0
    if climate in {"balanced", "moderate", "neutral"}:
        score = 82.0
    elif climate in {"warm", "hot", "cold", "cool"}:
        score = 70.0
    evidence_id = book.add_evidence(
        "climate_compatibility",
        "mc01.climate.consumed",
        source="canonical_temperature_engine",
        climate_state=context.climate_state,
    )
    classification = "supportive" if score >= 75 else "acceptable" if score >= 60 else "strained"
    return CompatibilityResult(
        state=AnalysisState.RESOLVED.value,
        classification=classification,
        score=score,
        evidence_ids=(evidence_id,),
        confidence=clamp_confidence(0.8),
    )
