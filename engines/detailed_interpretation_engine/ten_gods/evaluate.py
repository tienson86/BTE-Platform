"""Deterministic per-deity evaluation. No combinations, no MC-01 inference."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import (
    DayMasterBand,
    EvaluationStatus,
    HourCompleteness,
    TenGodConfidenceBand,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodRootState,
    TenGodStructuralRole,
    TenGodUsability,
    TenGodUsefulGodContext,
    TenGodVisibilitySummary,
)
from engines.detailed_interpretation_engine.ten_gods.constants import (
    CONDITION_HOUR_INCOMPLETE,
    CONDITION_MC01_NOT_BOUND,
    CONDITION_PATTERN_UNRESOLVED,
    CONDITION_USEFUL_GOD_UNRESOLVED,
    GOD_ID_TO_FAMILY,
    POSITIVE_CODES,
    RISK_CODES,
)
from engines.detailed_interpretation_engine.ten_gods.facts import (
    UpstreamTenGodFacts,
    pattern_mentions,
)
from engines.detailed_interpretation_engine.ten_gods.models import (
    TenGodInterpretationResult,
    TenGodOccurrence,
    TenGodVisibilityInventory,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def _visibility(occurrences: tuple[TenGodOccurrence, ...], hour_unknown: bool) -> TenGodVisibilityInventory:
    layers = {item.layer for item in occurrences}
    year_stem = "year_stem" in layers
    month_stem = "month_stem" in layers
    day_context = "day_context" in layers
    hour_stem = "hour_stem" in layers
    main_qi = "main_qi" in layers
    middle_qi = "middle_qi" in layers
    residual_qi = "residual_qi" in layers
    hidden = any(not item.visible for item in occurrences)
    exposed = any(item.visible for item in occurrences)
    if exposed and hidden:
        summary = TenGodVisibilitySummary.MIXED
    elif exposed:
        summary = TenGodVisibilitySummary.EXPOSED
    elif hidden:
        summary = TenGodVisibilitySummary.HIDDEN
    else:
        summary = TenGodVisibilitySummary.ABSENT
    return TenGodVisibilityInventory(
        year_stem=year_stem,
        month_stem=month_stem,
        day_context=day_context,
        hour_stem=hour_stem,
        branch_hidden=hidden,
        main_qi=main_qi,
        middle_qi=middle_qi,
        residual_qi=residual_qi,
        summary=summary,
        hour_unknown=hour_unknown,
    )


def _root_state(
    occurrences: tuple[TenGodOccurrence, ...],
    visibility: TenGodVisibilityInventory,
) -> TenGodRootState:
    if not occurrences:
        return TenGodRootState.NOT_APPLICABLE
    hidden = tuple(item for item in occurrences if not item.visible)
    visible = tuple(item for item in occurrences if item.visible)
    if visible and not hidden:
        return TenGodRootState.NO_ROOT
    layers = {item.layer for item in hidden}
    quality = 0
    if "residual_qi" in layers:
        quality = max(quality, 1)
    if "middle_qi" in layers:
        quality = max(quality, 2)
    if "main_qi" in layers:
        quality = max(quality, 3)
    if not hidden:
        return TenGodRootState.UNRESOLVED
    meaningful = [layer for layer in layers if layer in {"main_qi", "middle_qi"}]
    if len(meaningful) > 1 or (visibility.main_qi and visibility.middle_qi):
        return TenGodRootState.MULTIPLE_ROOTS
    if quality >= 3:
        return TenGodRootState.STRONG_ROOT
    if quality == 2:
        return TenGodRootState.MODERATE_ROOT
    return TenGodRootState.WEAK_ROOT


def _presence(
    occurrences: tuple[TenGodOccurrence, ...],
    visibility: TenGodVisibilityInventory,
    root: TenGodRootState,
    god_id: str,
    facts: UpstreamTenGodFacts,
) -> TenGodPresenceState:
    if not occurrences:
        return TenGodPresenceState.ABSENT
    visible = any(item.visible for item in occurrences)
    hidden = any(not item.visible for item in occurrences)
    if visible and root in {TenGodRootState.MODERATE_ROOT, TenGodRootState.STRONG_ROOT, TenGodRootState.MULTIPLE_ROOTS}:
        base = TenGodPresenceState.VISIBLE_AND_ROOTED
    elif visible:
        base = TenGodPresenceState.VISIBLE
    elif hidden:
        base = TenGodPresenceState.HIDDEN_ONLY
    else:
        return TenGodPresenceState.UNRESOLVED
    if god_id in facts.dominant_ids and base is TenGodPresenceState.VISIBLE_AND_ROOTED:
        return TenGodPresenceState.STRUCTURALLY_DOMINANT
    month_cluster = visibility.month_stem or visibility.main_qi
    other = visibility.year_stem or visibility.hour_stem or visibility.day_context
    if month_cluster and other and len(occurrences) > 1:
        return TenGodPresenceState.CONCENTRATED
    if len(occurrences) > 1:
        return TenGodPresenceState.REPEATED
    return base


def _effective_strength(
    presence: TenGodPresenceState,
    visibility: TenGodVisibilityInventory,
    root: TenGodRootState,
) -> TenGodEffectiveStrength:
    if presence is TenGodPresenceState.ABSENT:
        return TenGodEffectiveStrength.NOT_APPLICABLE
    if presence is TenGodPresenceState.UNRESOLVED:
        return TenGodEffectiveStrength.UNRESOLVED
    if presence is TenGodPresenceState.HIDDEN_ONLY and visibility.residual_qi and not visibility.main_qi:
        return TenGodEffectiveStrength.VERY_WEAK
    if presence is TenGodPresenceState.HIDDEN_ONLY:
        return TenGodEffectiveStrength.WEAK
    if presence is TenGodPresenceState.VISIBLE and root is TenGodRootState.NO_ROOT:
        return TenGodEffectiveStrength.WEAK
    if presence in {TenGodPresenceState.CONCENTRATED, TenGodPresenceState.STRUCTURALLY_DOMINANT}:
        if root in {TenGodRootState.STRONG_ROOT, TenGodRootState.MULTIPLE_ROOTS} and visibility.month_stem:
            return TenGodEffectiveStrength.VERY_STRONG
        return TenGodEffectiveStrength.STRONG
    if presence is TenGodPresenceState.VISIBLE_AND_ROOTED:
        if root is TenGodRootState.STRONG_ROOT and (visibility.month_stem or visibility.main_qi):
            return TenGodEffectiveStrength.STRONG
        return TenGodEffectiveStrength.MODERATE
    if presence is TenGodPresenceState.REPEATED:
        return TenGodEffectiveStrength.MODERATE
    return TenGodEffectiveStrength.WEAK


def _useful_god(god_id: str, facts: UpstreamTenGodFacts, presence: TenGodPresenceState) -> TenGodUsefulGodContext:
    if presence is TenGodPresenceState.ABSENT:
        return TenGodUsefulGodContext.NOT_APPLICABLE
    has_useful = bool(
        facts.useful_ten_god_ids
        or facts.favorable_ten_god_ids
        or facts.unfavorable_ten_god_ids
        or facts.useful_elements
        or facts.favorable_elements
        or facts.unfavorable_elements
    )
    if not has_useful:
        return TenGodUsefulGodContext.UNRESOLVED
    useful = god_id in facts.useful_ten_god_ids
    favorable = god_id in facts.favorable_ten_god_ids
    unfavorable = god_id in facts.unfavorable_ten_god_ids
    god_elements = {item.lower() for item in facts.elements.get(god_id, ())}
    if facts.useful_elements and god_elements.intersection({item.lower() for item in facts.useful_elements}):
        useful = True
    if facts.favorable_elements and god_elements.intersection({item.lower() for item in facts.favorable_elements}):
        favorable = True
    if facts.unfavorable_elements and god_elements.intersection(
        {item.lower() for item in facts.unfavorable_elements}
    ):
        unfavorable = True
    if (useful or favorable) and unfavorable:
        return TenGodUsefulGodContext.MIXED
    if useful:
        return TenGodUsefulGodContext.USEFUL
    if favorable:
        return TenGodUsefulGodContext.FAVORABLE
    if unfavorable:
        return TenGodUsefulGodContext.UNFAVORABLE
    return TenGodUsefulGodContext.NEUTRAL


def _structural_role(
    god_id: str,
    facts: UpstreamTenGodFacts,
    presence: TenGodPresenceState,
    dm: DayMasterBand,
) -> tuple[TenGodStructuralRole, str]:
    if presence is TenGodPresenceState.ABSENT:
        pattern = facts.pattern_text.strip() or "unresolved"
        return TenGodStructuralRole.UNRESOLVED, pattern if facts.pattern_text else "unresolved"
    if not facts.pattern_text:
        pattern_context = "unresolved"
        role = TenGodStructuralRole.UNRESOLVED
    elif pattern_mentions(facts.pattern_text, god_id):
        return TenGodStructuralRole.PRIMARY_PATTERN, facts.pattern_text
    else:
        pattern_context = facts.pattern_text
        role = TenGodStructuralRole.NEUTRAL
    family = GOD_ID_TO_FAMILY.get(god_id, "")
    if dm is DayMasterBand.WEAK and family in {"companion", "resource"}:
        role = TenGodStructuralRole.CAPACITY_SUPPORT
    elif dm is DayMasterBand.WEAK and family in {"wealth", "officer", "output"}:
        role = TenGodStructuralRole.CAPACITY_PRESSURE
    elif dm is DayMasterBand.STRONG and family == "resource":
        role = TenGodStructuralRole.CAPACITY_PRESSURE
    elif dm is DayMasterBand.STRONG and family == "companion":
        wealth_present = any(facts.occurrences.get(item) for item in ("pian_cai", "zheng_cai"))
        if wealth_present:
            role = TenGodStructuralRole.CAPACITY_PRESSURE
    return role, pattern_context


def _usability(
    presence: TenGodPresenceState,
    role: TenGodStructuralRole,
    useful: TenGodUsefulGodContext,
    strength: TenGodEffectiveStrength,
) -> TenGodUsability:
    if presence is TenGodPresenceState.ABSENT:
        return TenGodUsability.NOT_APPLICABLE
    if useful is TenGodUsefulGodContext.UNFAVORABLE and role is TenGodStructuralRole.CAPACITY_PRESSURE:
        return TenGodUsability.PRESSURING
    if role is TenGodStructuralRole.CAPACITY_PRESSURE:
        return TenGodUsability.PRESSURING
    if useful is TenGodUsefulGodContext.MIXED:
        return TenGodUsability.CONFLICTING
    if role is TenGodStructuralRole.CAPACITY_SUPPORT:
        return TenGodUsability.SUPPORTIVE
    if useful in {TenGodUsefulGodContext.USEFUL, TenGodUsefulGodContext.FAVORABLE}:
        if strength in {TenGodEffectiveStrength.WEAK, TenGodEffectiveStrength.VERY_WEAK}:
            return TenGodUsability.CONDITIONALLY_USABLE
        return TenGodUsability.USABLE
    if role is TenGodStructuralRole.PRIMARY_PATTERN:
        return TenGodUsability.USABLE
    if role is TenGodStructuralRole.UNRESOLVED:
        return TenGodUsability.UNRESOLVED
    return TenGodUsability.NEUTRAL


def _expressions(
    god_id: str,
    presence: TenGodPresenceState,
    strength: TenGodEffectiveStrength,
    usability: TenGodUsability,
    role: TenGodStructuralRole,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    if presence in {TenGodPresenceState.ABSENT, TenGodPresenceState.UNRESOLVED}:
        return (), ()
    positives: list[str] = []
    if strength in {
        TenGodEffectiveStrength.MODERATE,
        TenGodEffectiveStrength.STRONG,
        TenGodEffectiveStrength.VERY_STRONG,
    } and presence is not TenGodPresenceState.HIDDEN_ONLY:
        for code in POSITIVE_CODES.get(god_id, ()):
            if code == "carrying_capacity_support" and role is not TenGodStructuralRole.CAPACITY_SUPPORT:
                continue
            positives.append(code)
            if len(positives) >= 3:
                break
    risks: list[str] = []
    if usability in {TenGodUsability.PRESSURING, TenGodUsability.CONFLICTING, TenGodUsability.DAMAGING} or (
        strength in {TenGodEffectiveStrength.STRONG, TenGodEffectiveStrength.VERY_STRONG}
        and role is TenGodStructuralRole.CAPACITY_PRESSURE
    ):
        for code in RISK_CODES.get(god_id, ()):
            risks.append(code)
            if len(risks) >= 2:
                break
    return tuple(positives), tuple(risks)


def _confidence(
    facts: UpstreamTenGodFacts,
    presence: TenGodPresenceState,
    visibility: TenGodVisibilityInventory,
    pattern_context: str,
    useful: TenGodUsefulGodContext,
) -> ConfidenceValue:
    if presence is TenGodPresenceState.UNRESOLVED:
        band = TenGodConfidenceBand.UNRESOLVED
    elif not facts.mc01_bound or facts.hour_completeness is not HourCompleteness.COMPLETE:
        band = TenGodConfidenceBand.LOW
    elif presence is TenGodPresenceState.HIDDEN_ONLY and visibility.residual_qi and not visibility.main_qi:
        band = TenGodConfidenceBand.LOW
    elif pattern_context == "unresolved" or useful is TenGodUsefulGodContext.UNRESOLVED:
        band = TenGodConfidenceBand.MODERATE
    else:
        band = TenGodConfidenceBand.MODERATE
    return ConfidenceValue(value=None, summary=band.value)


def evaluate_ten_god(god_id: str, facts: UpstreamTenGodFacts) -> TenGodInterpretationResult:
    """Evaluate one canonical Ten God from consumed facts."""
    if not facts.available:
        return TenGodInterpretationResult(
            ten_god_id=god_id,
            state=EvaluationStatus.UNRESOLVED,
            presence_state=TenGodPresenceState.UNRESOLVED,
            pattern_context="unresolved",
            conditions=(CONDITION_MC01_NOT_BOUND,),
            trace_ids=(f"TR-P7-TG-{god_id}",),
            confidence=ConfidenceValue(summary=TenGodConfidenceBand.UNRESOLVED.value),
        )
    occurrences = facts.occurrences.get(god_id, ())
    hour_unknown = facts.hour_completeness is not HourCompleteness.COMPLETE
    visibility = _visibility(occurrences, hour_unknown)
    root = _root_state(occurrences, visibility)
    presence = _presence(occurrences, visibility, root, god_id, facts)
    strength = _effective_strength(presence, visibility, root)
    useful = _useful_god(god_id, facts, presence)
    role, pattern_context = _structural_role(god_id, facts, presence, facts.day_master_band)
    usability = _usability(presence, role, useful, strength)
    positives, risks = _expressions(god_id, presence, strength, usability, role)
    conditions: list[str] = []
    if not facts.mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    if hour_unknown:
        conditions.append(CONDITION_HOUR_INCOMPLETE)
    if pattern_context == "unresolved":
        conditions.append(CONDITION_PATTERN_UNRESOLVED)
    if useful is TenGodUsefulGodContext.UNRESOLVED:
        conditions.append(CONDITION_USEFUL_GOD_UNRESOLVED)
    state = EvaluationStatus.RESOLVED
    if presence is TenGodPresenceState.UNRESOLVED:
        state = EvaluationStatus.UNRESOLVED
    elif not facts.mc01_bound or useful is TenGodUsefulGodContext.UNRESOLVED or pattern_context == "unresolved":
        state = EvaluationStatus.PARTIALLY_RESOLVED
    elif presence is TenGodPresenceState.ABSENT:
        state = EvaluationStatus.RESOLVED
    evidence_ids = tuple(item.evidence_id for item in occurrences if item.evidence_id)
    trace_id = f"TR-P7-TG-{god_id}"
    return TenGodInterpretationResult(
        ten_god_id=god_id,
        state=state,
        presence_state=presence,
        occurrences=occurrences,
        visibility=visibility,
        root_state=root,
        effective_strength=strength,
        structural_role=role,
        day_master_context=facts.day_master_band,
        pattern_context=pattern_context,
        useful_god_context=useful,
        structural_usability=usability,
        positive_expressions=positives,
        risk_expressions=risks,
        conditions=tuple(conditions),
        evidence_ids=evidence_ids,
        trace_ids=(trace_id,),
        confidence=_confidence(facts, presence, visibility, pattern_context, useful),
        damage_ids=(),
        rescue_ids=(),
    )
