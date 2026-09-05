"""Career fit potentials. Not exact professions."""

from __future__ import annotations

from engines.mingju.constants import ACHIEVEMENT_BANDS
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.models import (
    AchievementProfile,
    CareerProfile,
    ProfileDimension,
    WealthProfile,
)
from engines.mingju.serialization import band_for_score, clamp_confidence


_FROM_ACHIEVEMENT = {
    "institutional_fit": "institutional_career",
    "entrepreneurial_fit": "entrepreneurship",
    "leadership_fit": "leadership",
    "management_fit": "management",
    "specialist_fit": "technical",
    "technical_fit": "technical",
    "academic_fit": "academic",
    "creative_fit": "creative",
    "public_facing_fit": "public_visibility",
    "autonomy_need": "independence",
    "career_stability": "stability",
}

_WORK_STYLES = {
    "institutional_fit": "structured_institutional",
    "entrepreneurial_fit": "entrepreneurial",
    "leadership_fit": "leadership_command",
    "management_fit": "managerial",
    "specialist_fit": "specialist",
    "technical_fit": "technical",
    "academic_fit": "academic_research",
    "creative_fit": "creative",
    "public_facing_fit": "public_facing",
    "autonomy_need": "independent",
}


def _score_map(profile: AchievementProfile) -> dict[str, float]:
    return {item.dimension: float(item.score or 0.0) for item in profile.dimensions}


def evaluate_career(
    achievement: AchievementProfile,
    wealth: WealthProfile,
    book: RecordBook,
) -> CareerProfile:
    """Career consumes Achievement. Entrepreneurial fit also reads Wealth context."""
    if achievement.state != AnalysisState.RESOLVED.value:
        return CareerProfile(state=AnalysisState.UNRESOLVED.value)
    scores = _score_map(achievement)
    wealth_scores = {item.dimension: float(item.score or 0.0) for item in wealth.dimensions}
    dimensions: list[ProfileDimension] = []
    for name, source in _FROM_ACHIEVEMENT.items():
        score = scores.get(source, 40.0)
        if name == "entrepreneurial_fit":
            creation = wealth_scores.get("wealth_creation", score)
            volatility = wealth_scores.get("financial_volatility", 50.0)
            score = round((score * 0.6) + (creation * 0.3) + ((100.0 - volatility) * 0.1), 2)
        evidence_id = book.add_evidence(
            "career",
            f"mc01.career.{name}",
            source="mingju.career",
            achievement_dimension=source,
            note="not_an_exact_profession",
        )
        dimensions.append(
            ProfileDimension(
                dimension=name,
                state=AnalysisState.RESOLVED.value,
                score=score,
                classification=band_for_score(score, ACHIEVEMENT_BANDS),
                confidence=clamp_confidence(achievement.confidence),
                evidence_ids=(evidence_id,),
            )
        )
    ranked = sorted(dimensions, key=lambda item: float(item.score or 0.0), reverse=True)
    styles = tuple(
        _WORK_STYLES[item.dimension]
        for item in ranked
        if item.dimension in _WORK_STYLES
    )[:3]
    evidence_ids = tuple(eid for item in dimensions for eid in item.evidence_ids)
    return CareerProfile(
        state=AnalysisState.RESOLVED.value,
        dimensions=tuple(dimensions),
        dominant_work_styles=styles,
        confidence=clamp_confidence(achievement.confidence),
        evidence_ids=evidence_ids,
    )
