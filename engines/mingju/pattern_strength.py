"""Pattern Strength. Distinct from Day Master Strength."""

from __future__ import annotations

from engines.mingju.constants import GOD_FAMILY, PATTERN_STRENGTH_BANDS, STRENGTH_DIMENSION_WEIGHTS
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power, god_power, is_material, normalize_god_id
from engines.mingju.models import MingJuContext, PatternDecision, PatternStrengthResult
from engines.mingju.serialization import band_for_score, clamp_confidence, clamp_score

_SEASON_BY_MONTH_GOD: dict[str, float] = {
    "aligned": 86.0,
    "family": 72.0,
    "neutral": 48.0,
    "conflict": 28.0,
}


def _season_power(context: MingJuContext, pattern: PatternDecision) -> float:
    month_god = normalize_god_id("", context.month_main_qi_ten_god)
    if month_god == pattern.pattern_id:
        return _SEASON_BY_MONTH_GOD["aligned"]
    if month_god and GOD_FAMILY.get(month_god, "") == GOD_FAMILY.get(pattern.pattern_id, ""):
        return _SEASON_BY_MONTH_GOD["family"]
    if month_god:
        return _SEASON_BY_MONTH_GOD["conflict"]
    return _SEASON_BY_MONTH_GOD["neutral"]


def _scale_activation(value: float, ceiling: float = 6.0) -> float:
    return clamp_score(100.0 * min(value, ceiling) / ceiling)


def evaluate_pattern_strength(
    context: MingJuContext,
    pattern: PatternDecision,
    book: RecordBook,
) -> PatternStrengthResult:
    """Evaluate power of the pattern deity, not of the Day Master."""
    if pattern.state != AnalysisState.RESOLVED.value or not pattern.pattern_id:
        return PatternStrengthResult(state=AnalysisState.UNRESOLVED.value, classification="unresolved")
    activations = context.activations
    pattern_id = pattern.pattern_id
    family = GOD_FAMILY.get(pattern_id, "")
    season = _season_power(context, pattern)
    root = _scale_activation(
        sum(
            item.activation
            for item in activations
            if item.god_id == pattern_id and item.layer != "visible"
        )
    )
    exposure = _scale_activation(
        sum(item.activation for item in activations if item.god_id == pattern_id and item.layer == "visible")
    )
    generating_family = {
        "companion": "resource",
        "output": "companion",
        "wealth": "output",
        "officer": "wealth",
        "resource": "officer",
    }.get(family, "")
    generation = _scale_activation(family_power(activations, generating_family) if generating_family else 0.0)
    continuity = 70.0 if is_material(activations, pattern_id) else 38.0
    if any(item.god_id == pattern_id and item.pillar == "month" for item in activations):
        continuity = min(100.0, continuity + 16.0)
    position = 42.0
    if any(item.god_id == pattern_id and item.pillar == "month" and item.material for item in activations):
        position = 84.0
    elif any(item.god_id == pattern_id and item.pillar == "hour" and item.layer == "visible" for item in activations):
        position = 68.0
    elif god_power(activations, pattern_id) > 0:
        position = 55.0
    dimensions = {
        "season_power": season,
        "root_power": root,
        "exposure_power": exposure,
        "generation_power": generation,
        "continuity_power": continuity,
        "position_power": position,
    }
    score = clamp_score(
        sum(value * STRENGTH_DIMENSION_WEIGHTS[name] for name, value in dimensions.items())
    )
    evidence_id = book.add_evidence(
        "pattern_strength",
        "mc01.pattern_strength.dimensions",
        source="mingju.pattern_strength",
        **{name: round(value, 2) for name, value in dimensions.items()},
        day_master_strength_level=context.day_master_strength_level,
        note="pattern_strength_is_not_day_master_strength",
    )
    book.add_trace("pattern_strength", "MC-STR-000", "mc01.pattern_strength.resolved", (evidence_id,))
    return PatternStrengthResult(
        state=AnalysisState.RESOLVED.value,
        classification=band_for_score(score, PATTERN_STRENGTH_BANDS),
        score=score,
        season_power=round(season, 2),
        root_power=round(root, 2),
        exposure_power=round(exposure, 2),
        generation_power=round(generation, 2),
        continuity_power=round(continuity, 2),
        position_power=round(position, 2),
        evidence_ids=(evidence_id,),
        confidence=clamp_confidence(0.86 if context.hour_present else 0.68),
    )
