"""Wealth structural capacity. Not 'Tài nhiều = giàu'."""

from __future__ import annotations

from engines.mingju.constants import ACHIEVEMENT_BANDS
from engines.mingju.enums import AnalysisState, IntegrityState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power, god_power
from engines.mingju.models import MingJuContext, ProfileDimension, StructuralIntegrityResult, WealthProfile
from engines.mingju.serialization import band_for_score, clamp_confidence, clamp_score


def _usable(raw: float, integrity: StructuralIntegrityResult) -> float:
    factor = 0.55 if integrity.score is None else max(0.35, float(integrity.score) / 100.0)
    return clamp_score(raw * factor + 16.0 * factor)


def evaluate_wealth(
    context: MingJuContext,
    integrity: StructuralIntegrityResult,
    book: RecordBook,
) -> WealthProfile:
    """Five frozen wealth dimensions. Volatility uses higher_is_riskier."""
    if integrity.state == IntegrityState.UNRESOLVED.value:
        return WealthProfile(state=AnalysisState.UNRESOLVED.value)
    activations = context.activations
    wealth = family_power(activations, "wealth")
    output = family_power(activations, "output")
    resource = family_power(activations, "resource")
    officer = family_power(activations, "officer")
    companion = family_power(activations, "companion")
    specs = (
        ("wealth_creation", 24 + output * 10 + wealth * 8, "higher_is_better"),
        ("wealth_accumulation", 24 + wealth * 10 + resource * 8, "higher_is_better"),
        ("wealth_retention", 26 + officer * 8 + resource * 10 - companion * 6, "higher_is_better"),
        ("business_expansion", 24 + output * 8 + companion * 8 + god_power(activations, "pian_cai") * 6, "higher_is_better"),
        ("financial_volatility", 20 + companion * 12 + output * 8 + god_power(activations, "jie_cai") * 6, "higher_is_riskier"),
    )
    dimensions: list[ProfileDimension] = []
    for name, raw, polarity in specs:
        score = _usable(raw, integrity)
        evidence_id = book.add_evidence(
            "wealth",
            f"mc01.wealth.{name}",
            source="mingju.wealth",
            raw=round(raw, 2),
            polarity=polarity,
            note="wealth_force_is_not_wealth_outcome",
        )
        dimensions.append(
            ProfileDimension(
                dimension=name,
                state=AnalysisState.RESOLVED.value,
                score=score,
                classification=band_for_score(score, ACHIEVEMENT_BANDS),
                polarity=polarity,
                confidence=clamp_confidence(integrity.confidence),
                evidence_ids=(evidence_id,),
            )
        )
    evidence_ids = tuple(eid for item in dimensions for eid in item.evidence_ids)
    return WealthProfile(
        state=AnalysisState.RESOLVED.value,
        dimensions=tuple(dimensions),
        confidence=clamp_confidence(integrity.confidence),
        evidence_ids=evidence_ids,
    )
