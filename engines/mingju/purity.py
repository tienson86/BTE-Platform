"""Pattern Purity. Independent of Pattern Strength, Damage, and Grade."""

from __future__ import annotations

from engines.mingju.constants import (
    COUNTERPART_PAIRS,
    GOD_FAMILY,
    PURITY_BANDS,
    PURITY_BASE_SCORE,
    PURITY_NEGATIVE_MAJOR,
    PURITY_NEGATIVE_MINOR,
    PURITY_NEGATIVE_MODERATE,
    PURITY_POSITIVE_MINOR,
    PURITY_POSITIVE_MODERATE,
)
from engines.mingju.enums import AnalysisState
from engines.mingju.evidence import RecordBook
from engines.mingju.facts import family_power, god_power, is_material, normalize_god_id
from engines.mingju.models import MingJuContext, PatternDecision, PatternPurityResult, PurityFactor
from engines.mingju.serialization import band_for_score, clamp_confidence, clamp_score


def _counterpart(pattern_id: str) -> str:
    for left, right in COUNTERPART_PAIRS:
        if pattern_id == left:
            return right
        if pattern_id == right:
            return left
    return ""


def evaluate_purity(
    context: MingJuContext,
    pattern: PatternDecision,
    book: RecordBook,
) -> PatternPurityResult:
    """Score structural mixing. Mixing is not Damage."""
    if pattern.state != AnalysisState.RESOLVED.value or not pattern.pattern_id:
        return PatternPurityResult(state=AnalysisState.UNRESOLVED.value, classification="unresolved")
    activations = context.activations
    pattern_id = pattern.pattern_id
    family = GOD_FAMILY.get(pattern_id, pattern.family)
    factors: list[PurityFactor] = []
    score = PURITY_BASE_SCORE

    def add_factor(
        factor_type: str,
        effect: str,
        severity: str,
        delta: float,
        rule_id: str,
    ) -> None:
        nonlocal score
        evidence_id = book.add_evidence(
            "purity",
            f"mc01.purity.{factor_type}",
            source="mingju.purity",
            pattern_id=pattern_id,
        )
        factor_id = book.next_id("E-MC-PUR")
        factors.append(
            PurityFactor(
                factor_id=factor_id,
                factor_type=factor_type,
                effect=effect,
                severity=severity,
                description_key=f"mc01.purity.{factor_type}",
                evidence_ids=(evidence_id,),
                rule_id=rule_id,
            )
        )
        score += delta if effect == "increase" else -delta

    if is_material(activations, pattern_id) or family_power(activations, family) > 0:
        add_factor("primary_deity_clear", "increase", "moderate", PURITY_POSITIVE_MODERATE, "MC-PUR-001")
    if any(item.god_id == pattern_id and item.layer == "visible" for item in activations):
        add_factor("primary_deity_exposed", "increase", "minor", PURITY_POSITIVE_MINOR, "MC-PUR-002")
    if any(item.god_id == pattern_id and item.layer in {"main_qi", "middle_qi"} for item in activations):
        add_factor("primary_deity_rooted", "increase", "minor", PURITY_POSITIVE_MINOR, "MC-PUR-003")
    month_god = normalize_god_id("", context.month_main_qi_ten_god)
    if month_god == pattern_id or GOD_FAMILY.get(month_god, "") == family:
        add_factor("month_command_consistent", "increase", "moderate", PURITY_POSITIVE_MODERATE, "MC-PUR-004")
    elif month_god:
        add_factor("month_command_conflict", "decrease", "moderate", PURITY_NEGATIVE_MODERATE, "MC-PUR-005")

    counterpart = _counterpart(pattern_id)
    if counterpart and is_material(activations, counterpart):
        severity = "major" if god_power(activations, counterpart) >= god_power(activations, pattern_id) else "moderate"
        delta = PURITY_NEGATIVE_MAJOR if severity == "major" else PURITY_NEGATIVE_MODERATE
        add_factor("counterpart_mixing", "decrease", severity, delta, "MC-PUR-006")
    elif counterpart and god_power(activations, counterpart) > 0:
        add_factor("counterpart_mixing", "decrease", "minor", PURITY_NEGATIVE_MINOR, "MC-PUR-007")

    competing = [
        item.god_id
        for item in activations
        if item.material and item.god_id != pattern_id and item.family != family
    ]
    unique_competing = tuple(dict.fromkeys(competing))
    if len(unique_competing) >= 2:
        add_factor("multiple_dominant_structures", "decrease", "major", PURITY_NEGATIVE_MAJOR, "MC-PUR-008")
    elif unique_competing:
        add_factor("competing_deity_visible", "decrease", "moderate", PURITY_NEGATIVE_MODERATE, "MC-PUR-009")

    if pattern.family == "follow":
        add_factor("single_structural_theme", "increase", "minor", PURITY_POSITIVE_MINOR, "MC-PUR-010")
    if not context.hour_present:
        add_factor("ambiguous_primary_theme", "decrease", "minor", PURITY_NEGATIVE_MINOR, "MC-PUR-011")

    score = clamp_score(score)
    classification = band_for_score(score, PURITY_BANDS)
    evidence_ids = tuple(eid for factor in factors for eid in factor.evidence_ids)
    book.add_trace("purity", "MC-PUR-000", "mc01.purity.resolved", evidence_ids)
    return PatternPurityResult(
        state=AnalysisState.RESOLVED.value,
        classification=classification,
        score=score,
        factors=tuple(factors),
        evidence_ids=evidence_ids,
        confidence=clamp_confidence(0.88 if context.hour_present else 0.7),
    )
