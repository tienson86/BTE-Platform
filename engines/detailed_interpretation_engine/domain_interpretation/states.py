"""Synthesize DomainState from copied MC-01 bands. No numeric score as sole truth."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domain_interpretation.constants import (
    BAND_TO_STATE,
    HIGH_BANDS,
    LOW_BANDS,
    MAJOR_DAMAGE_TYPES,
)
from engines.detailed_interpretation_engine.domain_interpretation.facts import DomainFacts, ProfileAxis
from engines.detailed_interpretation_engine.enums import DomainState

_BAND_RANK = {
    "very_high": 6,
    "high": 5,
    "above_average": 4,
    "moderate": 3,
    "average": 3,
    "below_average": 2,
    "low": 1,
    "very_low": 0,
}


def band_state(classification: str) -> DomainState:
    """Map one MC-01 band onto a frozen domain state."""
    return BAND_TO_STATE.get(classification, DomainState.UNRESOLVED)


def strongest_band(classifications: tuple[str, ...]) -> str:
    """Pick the strongest listed band without averaging."""
    present = [item for item in classifications if item in _BAND_RANK]
    if not present:
        return ""
    return max(present, key=lambda item: _BAND_RANK[item])


def weakest_band(classifications: tuple[str, ...]) -> str:
    """Pick the weakest listed band without averaging."""
    present = [item for item in classifications if item in _BAND_RANK]
    if not present:
        return ""
    return min(present, key=lambda item: _BAND_RANK[item])


def is_split(high: str, low: str) -> bool:
    """True when one axis is high and another is low."""
    return high in HIGH_BANDS and low in LOW_BANDS


def has_major_damage(facts: DomainFacts) -> bool:
    """True when MC-01 already recorded major/critical natal Damage."""
    return any(item in MAJOR_DAMAGE_TYPES or item.startswith("DMG-") for item in facts.damage_types)


def synthesize_state(
    classifications: tuple[str, ...],
    *,
    facts: DomainFacts,
    split: bool = False,
    missing: bool = False,
) -> DomainState:
    """Interpretive synthesis. High + unrescued Damage becomes conditional, not weak."""
    if missing:
        return DomainState.UNRESOLVED
    if split:
        return DomainState.FRAGMENTED
    band = strongest_band(classifications)
    if not band:
        return DomainState.UNRESOLVED
    state = band_state(band)
    if state in {DomainState.STRONG, DomainState.VERY_STRONG} and has_major_damage(facts):
        if not facts.has_rescue:
            return DomainState.CONDITIONAL
        return DomainState.CONDITIONAL
    return state


def axis_map(axes: dict[str, ProfileAxis], mapping: dict[str, str]) -> dict[str, str]:
    """Copy named MC-01 axes onto domain dimension keys."""
    result: dict[str, str] = {}
    for target, source in mapping.items():
        axis = axes.get(source)
        if axis is None or not axis.classification:
            continue
        result[target] = axis.classification
    return result
