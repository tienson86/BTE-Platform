"""Structural Integrity synthesis. Grade must consume this result."""

from __future__ import annotations

from engines.mingju.constants import (
    DAMAGE_SEVERITY_POINTS,
    INTEGRITY_WEIGHTS,
    RESCUE_OFFSET_POINTS,
)
from engines.mingju.enums import AnalysisState, IntegrityState
from engines.mingju.evidence import RecordBook
from engines.mingju.models import (
    CompatibilityResult,
    DamageResult,
    MingJuContext,
    PatternPurityResult,
    PatternStrengthResult,
    RescueResult,
    StructuralIntegrityResult,
    SupportResult,
)
from engines.mingju.serialization import clamp_confidence, clamp_score

_MAJOR = frozenset({"major", "critical"})


def _component(score: float | None, fallback: float = 50.0) -> float:
    return float(score) if score is not None else fallback


def evaluate_integrity(
    context: MingJuContext,
    purity: PatternPurityResult,
    strength: PatternStrengthResult,
    support: SupportResult,
    damage: DamageResult,
    rescue: RescueResult,
    useful_god: CompatibilityResult,
    climate: CompatibilityResult,
    book: RecordBook,
) -> StructuralIntegrityResult:
    """Combine purity, strength, support, residual damage, rescue, and compatibility."""
    if purity.state != AnalysisState.RESOLVED.value or strength.state != AnalysisState.RESOLVED.value:
        return StructuralIntegrityResult(state=IntegrityState.UNRESOLVED.value)
    damage_points = sum(DAMAGE_SEVERITY_POINTS.get(item.severity, 12.0) for item in damage.findings)
    rescued_ids = {target for item in rescue.findings for target in item.target_damage_ids}
    rescue_points = 0.0
    for item in rescue.findings:
        rescue_points += RESCUE_OFFSET_POINTS.get(item.strength, 8.0)
    residual_points = max(0.0, damage_points - rescue_points)
    residual_label = "none"
    if residual_points >= 40:
        residual_label = "critical"
    elif residual_points >= 24:
        residual_label = "major"
    elif residual_points >= 12:
        residual_label = "moderate"
    elif residual_points > 0:
        residual_label = "minor"
    damage_component = clamp_score(100.0 - residual_points)
    rescue_component = clamp_score(min(100.0, rescue_points * 2.2)) if damage.findings else 70.0
    purity_component = _component(purity.score)
    strength_component = _component(strength.score)
    support_component = _component(support.score)
    ug_component = _component(useful_god.score, 55.0)
    climate_component = _component(climate.score, 55.0)
    score = clamp_score(
        purity_component * INTEGRITY_WEIGHTS["purity"]
        + strength_component * INTEGRITY_WEIGHTS["pattern_strength"]
        + support_component * INTEGRITY_WEIGHTS["support"]
        + damage_component * INTEGRITY_WEIGHTS["damage"]
        + rescue_component * INTEGRITY_WEIGHTS["rescue"]
        + ug_component * INTEGRITY_WEIGHTS["useful_god"]
        + climate_component * INTEGRITY_WEIGHTS["climate"]
    )
    major_damage = tuple(item.damage_id for item in damage.findings if item.severity in _MAJOR)
    rescued_major = tuple(item_id for item_id in major_damage if item_id in rescued_ids)
    state = IntegrityState.SUBSTANTIALLY_COMPLETE.value
    if residual_label == "critical" and not rescued_major:
        state = IntegrityState.FAILED.value
    elif major_damage and rescued_major and residual_label in {"minor", "moderate", "none"}:
        state = IntegrityState.DAMAGED_BUT_RESCUED.value
    elif major_damage and not rescued_major:
        state = IntegrityState.DAMAGED.value
    elif residual_label in {"moderate", "minor"} and major_damage:
        state = IntegrityState.DAMAGED.value
    elif purity.classification in {"mixed", "heavily_mixed", "structurally_impure"} and not major_damage:
        state = IntegrityState.MIXED.value
    elif support.classification == "weak" or useful_god.classification == "conflicting":
        state = IntegrityState.CONDITIONALLY_COMPLETE.value
    elif (
        purity.classification in {"very_pure", "pure"}
        and strength.classification in {"strong", "very_strong"}
        and residual_label == "none"
    ):
        state = IntegrityState.COMPLETE.value
    if state == IntegrityState.FAILED.value and residual_label != "critical":
        state = IntegrityState.DAMAGED.value
    evidence_id = book.add_evidence(
        "integrity",
        "mc01.integrity.synthesis",
        source="mingju.integrity",
        residual_damage=residual_label,
        score=score,
    )
    book.add_trace("integrity", "MC-INT-000", "mc01.integrity.resolved", (evidence_id,))
    _ = context
    return StructuralIntegrityResult(
        state=state,
        score=score,
        classification=state,
        purity_component=round(purity_component, 2),
        strength_component=round(strength_component, 2),
        support_component=round(support_component, 2),
        damage_component=round(damage_component, 2),
        rescue_component=round(rescue_component, 2),
        useful_god_component=round(ug_component, 2),
        climate_component=round(climate_component, 2),
        residual_damage=residual_label,
        critical_findings=major_damage,
        evidence_ids=(evidence_id,),
        confidence=clamp_confidence(min(purity.confidence, strength.confidence, 0.9)),
    )
