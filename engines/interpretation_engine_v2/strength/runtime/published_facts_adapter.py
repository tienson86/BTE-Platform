"""Build PublishedStrengthFacts from live Strength Engine output."""

from __future__ import annotations

from engines.interpretation_engine_v2.strength.contracts.models import (
    EvidenceState,
    PublishedStrengthFacts,
)
from engines.strength_engine.context import StrengthContext
from engines.strength_engine.models import StrengthResult

EXECUTIVE_CONSULTING_NOT_AVAILABLE = "EXECUTIVE_CONSULTING_NOT_AVAILABLE"


def _score_state(score: float) -> EvidenceState:
    if score == 0.0:
        return EvidenceState.MISSING
    return EvidenceState.AVAILABLE


def _confidence_band(confidence: float) -> str:
    if confidence >= 0.8:
        return "high"
    if confidence >= 0.5:
        return "medium"
    return "low"


def build_published_strength_facts(
    *,
    case_id: str,
    strength_result: StrengthResult,
    strength_context: StrengthContext,
    luck_interaction_available: bool = False,
) -> PublishedStrengthFacts:
    """Map live StrengthResult + StrengthContext to PublishedStrengthFacts."""
    analysis = (strength_result.metadata or {}).get("trace", {}).get("analysis", {})
    special_matches = analysis.get("special_matches") or []

    root_level = strength_context.root_level or ""
    drain_count = int(strength_context.drain_count or 0)
    drain_type = strength_context.drain_type

    facts: dict[str, EvidenceState] = {
        "classification": (
            EvidenceState.AVAILABLE
            if strength_result.success
            else EvidenceState.INSUFFICIENT
        ),
        "season": _score_state(float(strength_result.season_score)),
        "root": (
            EvidenceState.AVAILABLE
            if root_level
            else _score_state(float(strength_result.root_score))
        ),
        "support": (
            EvidenceState.AVAILABLE
            if strength_context.support_type
            else _score_state(float(strength_result.support_score))
        ),
        "control": (
            EvidenceState.AVAILABLE
            if strength_context.control_type
            else _score_state(float(strength_result.control_score))
        ),
        "special": (
            EvidenceState.AVAILABLE
            if special_matches
            else EvidenceState.MISSING
        ),
        "combination": EvidenceState.NOT_APPLICABLE,
        "hidden_stems": EvidenceState.MISSING,
        "luck_interaction": (
            EvidenceState.AVAILABLE
            if luck_interaction_available
            else EvidenceState.MISSING
        ),
    }

    if "Thông căn 1 chi" in root_level:
        facts["root_thin"] = EvidenceState.AVAILABLE
    else:
        facts["root_thin"] = EvidenceState.MISSING

    if drain_count == 0 and drain_type is None:
        facts["drain"] = EvidenceState.INACTIVE
        facts["drain_active"] = EvidenceState.INACTIVE
    elif drain_count > 0 or drain_type:
        facts["drain"] = EvidenceState.AVAILABLE
        facts["drain_active"] = EvidenceState.AVAILABLE
    else:
        facts["drain"] = EvidenceState.MISSING

    forbidden_flags = {
        "drain_inactive": facts["drain"] == EvidenceState.INACTIVE,
        "root_thin": facts.get("root_thin") == EvidenceState.AVAILABLE,
        "root_deep_required": facts.get("root_thin") == EvidenceState.AVAILABLE,
        "luck_missing": facts["luck_interaction"] == EvidenceState.MISSING,
        "special_is_not_override": True,
    }

    conflicts: list[str] = []
    if forbidden_flags["root_thin"]:
        conflicts.append("C1")

    confidence = float(strength_result.confidence or 0.0)
    class_id = str(strength_result.strength_level or "balanced")
    interpretation_confidence = max(0, min(100, int(confidence * 72) or 72))

    return PublishedStrengthFacts(
        case_id=case_id or "UNASSIGNED",
        class_id=class_id,
        strength_score=float(strength_result.strength_score),
        facts=facts,
        polarities={
            "season": "support" if strength_result.season_score >= 0 else "weaken",
            "root": "support" if strength_result.root_score >= 0 else "weaken",
            "root_thin": "support",
            "support": "support" if strength_result.support_score >= 0 else "weaken",
            "control": "weaken" if strength_result.control_score <= 0 else "support",
            "special": "support" if special_matches else "neutral",
            "drain": "inactive" if facts["drain"] == EvidenceState.INACTIVE else "weaken",
        },
        forbidden_flags=forbidden_flags,
        interpretation_confidence=interpretation_confidence,
        confidence_band=_confidence_band(confidence),
        alternative_primary=class_id,
        alternative_runner_up="balanced",
        alternative_shares={},
        conflicts=conflicts,
    )
