"""Shared combination evaluation helpers. No dictionary meanings."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import (
    ChainQuality,
    CombinationReach,
    CombinationRelativePower,
    CombinationState,
    CombinationStructuralRole,
    DayMasterBand,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodUsefulGodContext,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.constants import FAMILY_MEMBERS
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    CombinationParticipant,
    TenGodChainFinding,
    TenGodChainLink,
)
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationResult

STRENGTH_RANK: dict[TenGodEffectiveStrength, int] = {
    TenGodEffectiveStrength.ABSENT: 0,
    TenGodEffectiveStrength.NOT_APPLICABLE: 0,
    TenGodEffectiveStrength.VERY_WEAK: 1,
    TenGodEffectiveStrength.WEAK: 2,
    TenGodEffectiveStrength.MODERATE: 3,
    TenGodEffectiveStrength.STRONG: 4,
    TenGodEffectiveStrength.VERY_STRONG: 5,
}

ACTIVE_STATES: frozenset[CombinationState] = frozenset(
    {
        CombinationState.CONFIRMED,
        CombinationState.CONDITIONAL,
        CombinationState.WEAK,
    }
)


def natal_index(
    items: tuple[TenGodInterpretationResult, ...],
) -> dict[str, TenGodInterpretationResult]:
    """Index natal results by canonical Ten God ID."""
    return {item.ten_god_id: item for item in items}


def is_present(item: TenGodInterpretationResult | None) -> bool:
    """True when the deity is not absent or unresolved."""
    if item is None:
        return False
    return item.presence_state not in {
        TenGodPresenceState.ABSENT,
        TenGodPresenceState.UNRESOLVED,
    }


def is_material(item: TenGodInterpretationResult | None) -> bool:
    """True when the deity can participate in an active relation."""
    if not is_present(item) or item is None:
        return False
    vis = item.visibility
    return bool(
        vis.year_stem
        or vis.month_stem
        or vis.day_context
        or vis.hour_stem
        or vis.main_qi
        or vis.middle_qi
    )


def is_residual_only(item: TenGodInterpretationResult | None) -> bool:
    """True when only residual hidden qi is present."""
    return is_present(item) and not is_material(item)


def rank_of(item: TenGodInterpretationResult | None) -> int | None:
    """Categorical strength rank. Unresolved stays incomparable."""
    if item is None:
        return 0
    if item.effective_strength is TenGodEffectiveStrength.UNRESOLVED:
        return None
    return STRENGTH_RANK.get(item.effective_strength, 0)


def family_items(
    index: dict[str, TenGodInterpretationResult],
    family: str,
) -> tuple[TenGodInterpretationResult, ...]:
    """Natal members of one functional family."""
    return tuple(index[god_id] for god_id in FAMILY_MEMBERS.get(family, ()) if god_id in index)


def best_member(
    items: tuple[TenGodInterpretationResult, ...],
    *,
    material_only: bool = False,
) -> TenGodInterpretationResult | None:
    """Strongest present member. Count is not used."""
    candidates = [item for item in items if is_present(item)]
    if material_only:
        candidates = [item for item in candidates if is_material(item)]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda item: (
            rank_of(item) or 0,
            1 if is_material(item) else 0,
            1 if item.visibility.month_stem or item.visibility.main_qi else 0,
        ),
    )


def relative_power(
    source: TenGodInterpretationResult | None,
    target: TenGodInterpretationResult | None,
    *,
    mediated: bool = False,
) -> CombinationRelativePower:
    """Compare DI-01 effective strength. Do not use occurrence count."""
    if mediated:
        return CombinationRelativePower.MEDIATED
    left = rank_of(source)
    right = rank_of(target)
    if left is None or right is None:
        return CombinationRelativePower.UNCERTAIN
    if left > right:
        return CombinationRelativePower.SOURCE_DOMINANT
    if right > left:
        return CombinationRelativePower.TARGET_DOMINANT
    return CombinationRelativePower.BALANCED


def quality_from_ranks(ranks: tuple[int, ...]) -> ChainQuality:
    """Weakest-link quality. Zero rank is a broken node."""
    if not ranks or any(rank <= 0 for rank in ranks):
        return ChainQuality.BROKEN
    weakest = min(ranks)
    if weakest <= 1:
        return ChainQuality.VERY_WEAK
    if weakest == 2:
        return ChainQuality.WEAK
    if weakest == 3:
        return ChainQuality.FUNCTIONAL
    if weakest == 4:
        return ChainQuality.STRONG
    return ChainQuality.VERY_STRONG


def meets_min_strength(item: TenGodInterpretationResult | None, minimum: str) -> bool:
    """True when categorical strength meets a named floor."""
    rank = rank_of(item) or 0
    if minimum == "strong":
        return rank >= STRENGTH_RANK[TenGodEffectiveStrength.STRONG]
    if minimum == "moderate":
        return rank >= STRENGTH_RANK[TenGodEffectiveStrength.MODERATE]
    return rank > 0


def dm_matches(band: DayMasterBand, required: str) -> bool:
    """True when consumed Day Master band matches a use/capacity rule."""
    if not required:
        return True
    if required == "weak":
        return band is DayMasterBand.WEAK
    if required == "strong":
        return band is DayMasterBand.STRONG
    return False


def as_participant(item: TenGodInterpretationResult, role: str) -> CombinationParticipant:
    """Copy natal facts onto a combination participant."""
    return CombinationParticipant(
        ten_god_id=item.ten_god_id,
        role_in_combination=role,
        effective_strength=item.effective_strength,
        visibility=item.visibility.summary,
        root_state=item.root_state,
        structural_role=item.structural_role,
    )


def carrier_participant(band: DayMasterBand) -> CombinationParticipant:
    """Day Master as capacity carrier, not a Ten God identity."""
    strength = {
        DayMasterBand.WEAK: TenGodEffectiveStrength.WEAK,
        DayMasterBand.MODERATE: TenGodEffectiveStrength.MODERATE,
        DayMasterBand.STRONG: TenGodEffectiveStrength.STRONG,
    }.get(band, TenGodEffectiveStrength.UNRESOLVED)
    return CombinationParticipant(
        ten_god_id="day_master",
        role_in_combination="carrier",
        effective_strength=strength,
    )


def two_node_chain(
    chain_id: str,
    source: TenGodInterpretationResult,
    target: TenGodInterpretationResult,
    vector: str,
    quality: ChainQuality,
    reach: CombinationReach,
    link_state: str,
) -> TenGodChainFinding:
    """Build a preserved A→B chain."""
    weakest = source.ten_god_id if (rank_of(source) or 0) <= (rank_of(target) or 0) else target.ten_god_id
    broken = () if link_state not in {"broken", "blocked"} else (f"{source.ten_god_id}->{target.ten_god_id}",)
    return TenGodChainFinding(
        chain_id=chain_id,
        nodes=(source.ten_god_id, target.ten_god_id),
        links=(
            TenGodChainLink(
                source=source.ten_god_id,
                target=target.ten_god_id,
                vector=vector,
                reach=reach,
                state=link_state,
            ),
        ),
        quality=quality,
        weakest_link=weakest,
        broken_link_ids=broken,
    )


def useful_of(*items: TenGodInterpretationResult | None) -> TenGodUsefulGodContext:
    """Combine consumed Useful God context. Do not infer Dụng/Hỷ/Kỵ."""
    values = [item.useful_god_context for item in items if item is not None]
    if not values:
        return TenGodUsefulGodContext.UNRESOLVED
    if TenGodUsefulGodContext.UNRESOLVED in values:
        return TenGodUsefulGodContext.UNRESOLVED
    if TenGodUsefulGodContext.UNFAVORABLE in values and (
        TenGodUsefulGodContext.USEFUL in values or TenGodUsefulGodContext.FAVORABLE in values
    ):
        return TenGodUsefulGodContext.MIXED
    if TenGodUsefulGodContext.USEFUL in values:
        return TenGodUsefulGodContext.USEFUL
    if TenGodUsefulGodContext.FAVORABLE in values:
        return TenGodUsefulGodContext.FAVORABLE
    if TenGodUsefulGodContext.UNFAVORABLE in values:
        return TenGodUsefulGodContext.UNFAVORABLE
    return TenGodUsefulGodContext.NEUTRAL


def pattern_of(*items: TenGodInterpretationResult | None) -> str:
    """Reuse natal Pattern context. Do not elect Pattern."""
    for item in items:
        if item is not None and item.pattern_context and item.pattern_context != "unresolved":
            return item.pattern_context
    return "unresolved"


def structural_role_for(
    items: tuple[TenGodInterpretationResult, ...],
    state: CombinationState,
) -> CombinationStructuralRole:
    """Pattern-mentioned participants raise importance. Names do not."""
    if state is CombinationState.INACTIVE:
        return CombinationStructuralRole.INCIDENTAL_RELATION
    if any(item.structural_role.value == "primary_pattern" for item in items if is_present(item)):
        return CombinationStructuralRole.PRIMARY_STRUCTURAL_CHAIN
    if state in ACTIVE_STATES:
        return CombinationStructuralRole.SUPPORTING_CHAIN
    return CombinationStructuralRole.UNRESOLVED


def generation_state(quality: ChainQuality, *, residual: bool) -> CombinationState:
    """Map chain quality to combination state for meaning-modifier generation."""
    if residual:
        return CombinationState.INACTIVE
    if quality is ChainQuality.BROKEN:
        return CombinationState.BROKEN
    if quality in {ChainQuality.VERY_WEAK, ChainQuality.WEAK}:
        return CombinationState.WEAK
    if quality is ChainQuality.CONDITIONAL:
        return CombinationState.CONDITIONAL
    if quality is ChainQuality.UNRESOLVED:
        return CombinationState.UNRESOLVED
    return CombinationState.CONFIRMED
