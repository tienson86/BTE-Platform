"""Achievement potentials. Not biography or guaranteed status."""

from __future__ import annotations

from engines.mingju.constants import ACHIEVEMENT_BANDS, GOD_FAMILY
from engines.mingju.enums import AnalysisState, IntegrityState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power, god_power
from engines.mingju.models import (
    AchievementProfile,
    MingJuContext,
    PatternDecision,
    PatternGradeResult,
    ProfileDimension,
    StructuralIntegrityResult,
)
from engines.mingju.serialization import band_for_score, clamp_confidence, clamp_score

_DIMENSIONS = (
    "authority",
    "institutional_career",
    "leadership",
    "management",
    "entrepreneurship",
    "academic",
    "technical",
    "creative",
    "public_visibility",
    "independence",
    "stability",
)


def _usable(raw: float, integrity: StructuralIntegrityResult) -> float:
    factor = 0.55 if integrity.score is None else max(0.35, float(integrity.score) / 100.0)
    return clamp_score(raw * factor + 18.0 * factor)


def evaluate_achievement(
    context: MingJuContext,
    pattern: PatternDecision,
    integrity: StructuralIntegrityResult,
    grade: PatternGradeResult,
    book: RecordBook,
) -> AchievementProfile:
    """Multi-dimensional capability profile downstream of Integrity."""
    if integrity.state == IntegrityState.UNRESOLVED.value:
        return AchievementProfile(state=AnalysisState.UNRESOLVED.value)
    activations = context.activations
    officer = family_power(activations, "officer")
    resource = family_power(activations, "resource")
    output = family_power(activations, "output")
    wealth = family_power(activations, "wealth")
    companion = family_power(activations, "companion")
    raw = {
        "authority": 28 + officer * 14 + god_power(activations, "zheng_guan") * 6,
        "institutional_career": 26 + god_power(activations, "zheng_guan") * 12 + resource * 8,
        "leadership": 26 + god_power(activations, "qi_sha") * 12 + officer * 6,
        "management": 24 + officer * 8 + resource * 8,
        "entrepreneurship": 24 + companion * 10 + wealth * 8 + god_power(activations, "jie_cai") * 6,
        "academic": 24 + resource * 12 + god_power(activations, "zheng_yin") * 6,
        "technical": 24 + god_power(activations, "shi_shen") * 12 + resource * 6,
        "creative": 24 + output * 12 + god_power(activations, "shang_guan") * 8,
        "public_visibility": 22 + god_power(activations, "shang_guan") * 12 + output * 6,
        "independence": 24 + companion * 12 + output * 6,
        "stability": 26 + resource * 10 + god_power(activations, "zheng_guan") * 6 - companion * 4,
    }
    _ = pattern
    _ = grade
    dimensions: list[ProfileDimension] = []
    for name in _DIMENSIONS:
        score = _usable(raw[name], integrity)
        evidence_id = book.add_evidence(
            "achievement",
            f"mc01.achievement.{name}",
            source="mingju.achievement",
            raw=round(raw[name], 2),
            usable=score,
        )
        dimensions.append(
            ProfileDimension(
                dimension=name,
                state=AnalysisState.RESOLVED.value,
                score=score,
                classification=band_for_score(score, ACHIEVEMENT_BANDS),
                confidence=clamp_confidence(integrity.confidence),
                evidence_ids=(evidence_id,),
            )
        )
    ranked = sorted(dimensions, key=lambda item: float(item.score or 0.0), reverse=True)
    risks: list[str] = []
    if integrity.residual_damage in {"major", "critical"}:
        risks.append("residual_structural_damage")
    if GOD_FAMILY.get(pattern.pattern_id) == "officer" and family_power(activations, "output") >= 3:
        risks.append("authority_expression_friction")
    evidence_ids = tuple(eid for item in dimensions for eid in item.evidence_ids)
    return AchievementProfile(
        state=AnalysisState.RESOLVED.value,
        dimensions=tuple(dimensions),
        dominant_capabilities=tuple(item.dimension for item in ranked[:3]),
        secondary_capabilities=tuple(item.dimension for item in ranked[3:6]),
        structural_risks=tuple(risks),
        conditions_for_expression=("integrity_must_hold", "luck_activation_required"),
        confidence=clamp_confidence(integrity.confidence),
        evidence_ids=evidence_ids,
    )
