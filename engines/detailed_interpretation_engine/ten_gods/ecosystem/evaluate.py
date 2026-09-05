"""DI-04 ecosystem evaluation. Driver is not frequency. Bottleneck belongs to an active chain."""

from __future__ import annotations

from engines.detailed_interpretation_engine.enums import (
    CombinationState,
    EcosystemRole,
    EcosystemState,
    EvaluationStatus,
    FlowQuality,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodStructuralRole,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.helpers import (
    ACTIVE_STATES,
    is_material,
    is_present,
    natal_index,
    rank_of,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    TenGodCombinationCollection,
    TenGodCombinationResult,
)
from engines.detailed_interpretation_engine.ten_gods.ecosystem.constants import (
    CONDITION_MC01_NOT_BOUND,
    CONDITION_NO_ACTIVE_CHAIN,
    CONDITION_PATTERN_UNRESOLVED,
    CONDITION_UNRESOLVED_DRIVER,
    FAMILY_GODS,
    FAMILY_ORDER,
    GENERATION_FLOW_IDS,
)
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import (
    EcosystemFlow,
    EcosystemRoleAssignment,
    FamilyBalance,
    TenGodEcosystemResult,
)
from engines.detailed_interpretation_engine.ten_gods.models import (
    TenGodInterpretationCollection,
    TenGodInterpretationResult,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_NA = EvaluationStatus.NOT_APPLICABLE
_UNRESOLVED = EvaluationStatus.UNRESOLVED
_ASSIGNED = EvaluationStatus.RESOLVED


def _empty_role(role: EcosystemRole, *, state: EvaluationStatus = _NA) -> EcosystemRoleAssignment:
    return EcosystemRoleAssignment(role=role, state=state, basis=())


def _family_of(god_id: str) -> str:
    for family, members in FAMILY_GODS.items():
        if god_id in members:
            return family
    return ""


def _family_rank(index: dict[str, TenGodInterpretationResult], family: str) -> int:
    ranks = [rank_of(index.get(god_id)) or 0 for god_id in FAMILY_GODS[family]]
    return max(ranks, default=0)


def _family_present(index: dict[str, TenGodInterpretationResult], family: str) -> bool:
    return any(is_present(index.get(god_id)) for god_id in FAMILY_GODS[family])


def _family_material(index: dict[str, TenGodInterpretationResult], family: str) -> bool:
    return any(is_material(index.get(god_id)) for god_id in FAMILY_GODS[family])


def _active(items: tuple[TenGodCombinationResult, ...]) -> tuple[TenGodCombinationResult, ...]:
    return tuple(item for item in items if item.state in ACTIVE_STATES)


def _map_quality(quality: str) -> FlowQuality:
    mapping = {
        "broken": FlowQuality.BROKEN,
        "very_weak": FlowQuality.RESTRICTED,
        "weak": FlowQuality.RESTRICTED,
        "conditional": FlowQuality.CONDITIONAL,
        "functional": FlowQuality.FUNCTIONAL,
        "strong": FlowQuality.STRONG,
        "very_strong": FlowQuality.STRONG,
        "unresolved": FlowQuality.UNRESOLVED,
    }
    return mapping.get(quality, FlowQuality.UNRESOLVED)


def _driver(
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
) -> EcosystemRoleAssignment:
    """Structural momentum. Pattern primary if material. Never occurrence count."""
    pattern_items = [
        item
        for item in natal.items
        if item.structural_role is TenGodStructuralRole.PRIMARY_PATTERN and is_material(item)
    ]
    if pattern_items:
        chosen = max(pattern_items, key=lambda item: rank_of(item) or 0)
        return EcosystemRoleAssignment(
            subject=chosen.ten_god_id,
            subject_kind="ten_god",
            role=EcosystemRole.DRIVER,
            state=_ASSIGNED if mc01_bound else EvaluationStatus.PARTIALLY_RESOLVED,
            basis=("pattern_primary", "effective_strength", "not_occurrence_count"),
            evidence_ids=chosen.evidence_ids,
            confidence=ConfidenceValue(summary="low" if not mc01_bound else "moderate"),
        )
    generators = [
        item
        for item in natal.items
        if item.structural_role is TenGodStructuralRole.PATTERN_GENERATOR and is_material(item)
    ]
    if generators:
        chosen = generators[0]
        return EcosystemRoleAssignment(
            subject=chosen.ten_god_id,
            subject_kind="ten_god",
            role=EcosystemRole.DRIVER,
            state=EvaluationStatus.PARTIALLY_RESOLVED,
            basis=("pattern_generator", "not_occurrence_count"),
            evidence_ids=chosen.evidence_ids,
            confidence=ConfidenceValue(summary="low"),
        )
    pattern_text = next((item.pattern_context for item in natal.items if item.pattern_context != "unresolved"), "")
    basis: tuple[str, ...] = (CONDITION_UNRESOLVED_DRIVER, "not_occurrence_count")
    if not pattern_text:
        basis = (CONDITION_PATTERN_UNRESOLVED, "not_occurrence_count")
    if not mc01_bound:
        basis = basis + (CONDITION_MC01_NOT_BOUND,)
    return EcosystemRoleAssignment(
        subject="",
        subject_kind="ten_god",
        role=EcosystemRole.DRIVER,
        state=_UNRESOLVED,
        basis=basis,
        confidence=ConfidenceValue(summary="unresolved"),
    )


def _support(
    active: tuple[TenGodCombinationResult, ...],
    driver: EcosystemRoleAssignment,
) -> EcosystemRoleAssignment:
    if driver.state is _UNRESOLVED or not driver.subject:
        generation = [item for item in active if "generation_chain" in item.combination_type]
        if not generation:
            return _empty_role(EcosystemRole.SUPPORTING)
        chosen = generation[0]
        subject = chosen.source or chosen.target
        return EcosystemRoleAssignment(
            subject=subject,
            subject_kind="ten_god",
            role=EcosystemRole.SUPPORTING,
            state=EvaluationStatus.PARTIALLY_RESOLVED,
            basis=("active_generation_chain",),
            source_chain_ids=(chosen.chain.chain_id,),
            evidence_ids=chosen.evidence_ids,
            confidence=ConfidenceValue(summary="low"),
        )
    for item in active:
        if item.target == driver.subject and "generation_chain" in item.combination_type:
            return EcosystemRoleAssignment(
                subject=item.source,
                subject_kind="ten_god",
                role=EcosystemRole.SUPPORTING,
                state=_ASSIGNED,
                basis=("generates_driver", "active_combination"),
                source_chain_ids=(item.chain.chain_id,),
                evidence_ids=item.evidence_ids,
                confidence=ConfidenceValue(summary="moderate"),
            )
    uses = [item for item in active if item.relationship == "uses"]
    if uses:
        chosen = uses[0]
        return EcosystemRoleAssignment(
            subject=chosen.target,
            subject_kind="ten_god",
            role=EcosystemRole.SUPPORTING,
            state=_ASSIGNED,
            basis=("use_chain",),
            source_chain_ids=(chosen.chain.chain_id,),
            evidence_ids=chosen.evidence_ids,
            confidence=ConfidenceValue(summary="moderate"),
        )
    return _empty_role(EcosystemRole.SUPPORTING)


def _bottleneck(active: tuple[TenGodCombinationResult, ...]) -> EcosystemRoleAssignment:
    """Weakest necessary link inside an active valuable chain. Not globally weakest deity."""
    candidates = [
        item
        for item in active
        if item.combination_id in GENERATION_FLOW_IDS or item.relationship in {"generates", "uses"}
    ]
    if not candidates:
        return EcosystemRoleAssignment(
            role=EcosystemRole.BOTTLENECK,
            state=_NA,
            basis=(CONDITION_NO_ACTIVE_CHAIN,),
            confidence=ConfidenceValue(summary="low"),
        )
    primary = max(
        candidates,
        key=lambda item: (len(item.chain.nodes), 1 if item.state is CombinationState.CONFIRMED else 0),
    )
    subject = primary.chain.weakest_link or primary.target or primary.source
    kind = "family" if subject in FAMILY_GODS else "ten_god"
    if subject == "day_master":
        kind = "day_master"
    return EcosystemRoleAssignment(
        subject=subject,
        subject_kind=kind,
        role=EcosystemRole.BOTTLENECK,
        state=_ASSIGNED,
        basis=("active_chain_weakest_link", "not_globally_weakest"),
        source_chain_ids=(primary.chain.chain_id,),
        evidence_ids=primary.evidence_ids,
        confidence=ConfidenceValue(summary="moderate"),
    )


def _blocked(
    index: dict[str, TenGodInterpretationResult],
    combinations: tuple[TenGodCombinationResult, ...],
) -> EcosystemRoleAssignment:
    output_rank = _family_rank(index, "output")
    wealth_rank = _family_rank(index, "wealth")
    output_material = _family_material(index, "output")
    wealth_present = _family_present(index, "wealth")
    output_to_wealth = [
        item
        for item in combinations
        if item.combination_id in {"shi_shen_generates_wealth", "shang_guan_generates_wealth"}
    ]
    indicated = output_material and output_rank >= 3
    cannot_continue = indicated and (not wealth_present or wealth_rank <= 1)
    broken = any(item.state is CombinationState.BROKEN and item.source for item in output_to_wealth)
    if not (cannot_continue or (indicated and broken)):
        return _empty_role(EcosystemRole.BLOCKED)
    source = next(
        (item for item in output_to_wealth if item.source),
        None,
    )
    subject = source.source if source else next(
        (god_id for god_id in FAMILY_GODS["output"] if is_material(index.get(god_id))),
        "output",
    )
    chain_ids = tuple(item.chain.chain_id for item in output_to_wealth if item.chain.chain_id)
    return EcosystemRoleAssignment(
        subject=subject,
        subject_kind="ten_god" if subject not in FAMILY_ORDER else "family",
        role=EcosystemRole.BLOCKED,
        state=_ASSIGNED,
        basis=("output_cannot_convert_to_wealth", "chain_evidence"),
        source_chain_ids=chain_ids,
        confidence=ConfidenceValue(summary="moderate"),
    )


def _excessive(
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
) -> EcosystemRoleAssignment:
    pressuring = [
        item
        for item in natal.items
        if item.structural_role is TenGodStructuralRole.CAPACITY_PRESSURE
        and item.effective_strength in {TenGodEffectiveStrength.STRONG, TenGodEffectiveStrength.VERY_STRONG}
        and item.structural_role is not TenGodStructuralRole.PRIMARY_PATTERN
    ]
    if not pressuring:
        return _empty_role(EcosystemRole.EXCESSIVE)
    chosen = max(pressuring, key=lambda item: rank_of(item) or 0)
    family = _family_of(chosen.ten_god_id)
    return EcosystemRoleAssignment(
        subject=family or chosen.ten_god_id,
        subject_kind="family" if family else "ten_god",
        role=EcosystemRole.EXCESSIVE,
        state=_ASSIGNED,
        basis=("capacity_pressure", "effective_strength", "not_raw_count"),
        evidence_ids=chosen.evidence_ids,
        confidence=ConfidenceValue(summary="moderate"),
    )


def _deficient_missing(
    index: dict[str, TenGodInterpretationResult],
    active: tuple[TenGodCombinationResult, ...],
    bottleneck: EcosystemRoleAssignment,
    hour_incomplete: bool,
) -> tuple[EcosystemRoleAssignment, EcosystemRoleAssignment]:
    needed: set[str] = set()
    for item in active:
        for node in item.chain.nodes:
            family = node if node in FAMILY_GODS else _family_of(node)
            if family:
                needed.add(family)
    deficient = _empty_role(EcosystemRole.DEFICIENT)
    missing = _empty_role(EcosystemRole.MISSING)
    for family in FAMILY_ORDER:
        rank = _family_rank(index, family)
        present = _family_present(index, family)
        if present and rank <= 2 and (family in needed or bottleneck.subject in FAMILY_GODS.get(family, ())):
            deficient = EcosystemRoleAssignment(
                subject=family,
                subject_kind="family",
                role=EcosystemRole.DEFICIENT,
                state=_ASSIGNED,
                basis=("needed_function_too_weak", "not_wish_for_every_star"),
                source_chain_ids=bottleneck.source_chain_ids,
                confidence=ConfidenceValue(summary="moderate"),
            )
            break
    for family in FAMILY_ORDER:
        if _family_present(index, family):
            continue
        if hour_incomplete:
            missing = EcosystemRoleAssignment(
                subject=family,
                subject_kind="family",
                role=EcosystemRole.MISSING,
                state=_UNRESOLVED,
                basis=("hour_unknown_absence_not_proven",),
                confidence=ConfidenceValue(summary="unresolved"),
            )
            break
        if family in needed:
            missing = EcosystemRoleAssignment(
                subject=family,
                subject_kind="family",
                role=EcosystemRole.MISSING,
                state=_ASSIGNED,
                basis=("functional_absence", "missing_not_unfavorable"),
                confidence=ConfidenceValue(summary="moderate"),
            )
            break
    return deficient, missing


def _neutral(
    natal: TenGodInterpretationCollection,
    assigned: set[str],
) -> tuple[EcosystemRoleAssignment, ...]:
    found: list[EcosystemRoleAssignment] = []
    for item in natal.items:
        if not is_present(item):
            continue
        if item.ten_god_id in assigned or _family_of(item.ten_god_id) in assigned:
            continue
        if item.presence_state is TenGodPresenceState.HIDDEN_ONLY and not is_material(item):
            found.append(
                EcosystemRoleAssignment(
                    subject=item.ten_god_id,
                    subject_kind="ten_god",
                    role=EcosystemRole.NEUTRAL,
                    state=_ASSIGNED,
                    basis=("incidental_residual",),
                    evidence_ids=item.evidence_ids,
                    confidence=ConfidenceValue(summary="low"),
                )
            )
    return tuple(found)


def _family_balances(index: dict[str, TenGodInterpretationResult]) -> tuple[FamilyBalance, ...]:
    rows: list[FamilyBalance] = []
    for family in FAMILY_ORDER:
        rank = _family_rank(index, family)
        present = _family_present(index, family)
        if not present:
            state = "missing"
            dominance = "non_contributing"
        elif rank <= 2:
            state = "deficient"
            dominance = "minor"
        elif rank == 3:
            state = "balanced"
            dominance = "material"
        elif rank == 4:
            state = "strong"
            dominance = "dominant"
        else:
            state = "very_strong"
            dominance = "dominant"
        rows.append(
            FamilyBalance(
                family_id=family,
                state=state,
                dominance=dominance,
                notes_key="not_occurrence_count",
                confidence=ConfidenceValue(summary="moderate"),
            )
        )
    return tuple(rows)


def _flows(active: tuple[TenGodCombinationResult, ...]) -> tuple[EcosystemFlow, ...]:
    flows: list[EcosystemFlow] = []
    for item in active:
        if item.combination_id not in GENERATION_FLOW_IDS and item.relationship != "generates":
            continue
        nodes = item.chain.nodes or tuple(part for part in (item.source, item.mediator, item.target) if part)
        if len(nodes) < 2:
            continue
        flows.append(
            EcosystemFlow(
                flow_id=item.combination_id,
                nodes=nodes,
                source_chain_ids=(item.chain.chain_id,),
                quality=_map_quality(item.chain_quality.value),
            )
        )
    return tuple(flows)


def _ecosystem_state(
    driver: EcosystemRoleAssignment,
    bottleneck: EcosystemRoleAssignment,
    blocked: EcosystemRoleAssignment,
    flow_quality: FlowQuality,
    mc01_bound: bool,
) -> EcosystemState:
    if driver.state is _UNRESOLVED:
        return EcosystemState.UNRESOLVED
    if flow_quality is FlowQuality.BROKEN or blocked.state is _ASSIGNED:
        return EcosystemState.BLOCKED
    if bottleneck.state is _ASSIGNED:
        return EcosystemState.MODERATELY_UNBALANCED
    if not mc01_bound:
        return EcosystemState.SLIGHTLY_UNBALANCED
    if flow_quality in {FlowQuality.STRONG, FlowQuality.FUNCTIONAL}:
        return EcosystemState.BALANCED
    return EcosystemState.SLIGHTLY_UNBALANCED


def evaluate_ecosystem(
    natal: TenGodInterpretationCollection,
    combinations: TenGodCombinationCollection,
    *,
    mc01_bound: bool,
) -> TenGodEcosystemResult:
    """Synthesize natal + active combinations into one ecosystem reading."""
    index = natal_index(natal.items)
    hour_incomplete = any("hour_pillar_incomplete" in item.conditions for item in natal.items)
    active = _active(combinations.items)
    driver = _driver(natal, index, mc01_bound)
    support = _support(active, driver)
    bottleneck = _bottleneck(active)
    blocked = _blocked(index, combinations.items)
    suppressed = _empty_role(EcosystemRole.SUPPRESSED)
    if any(item.combination_id == "owl_robs_food_combination" and item.state is CombinationState.UNRESOLVED for item in combinations.items):
        owl = next(item for item in combinations.items if item.combination_id == "owl_robs_food_combination")
        if owl.target:
            suppressed = EcosystemRoleAssignment(
                subject=owl.target,
                subject_kind="ten_god",
                role=EcosystemRole.SUPPRESSED,
                state=_UNRESOLVED,
                basis=("control_candidate_mc01_unbound", "not_dictionary_opposition"),
                source_chain_ids=(owl.chain.chain_id,),
                confidence=ConfidenceValue(summary="low"),
            )
    excessive = _excessive(natal, index)
    deficient, missing = _deficient_missing(index, active, bottleneck, hour_incomplete)
    balancer = _empty_role(EcosystemRole.BALANCER)
    assigned = {
        driver.subject,
        support.subject,
        bottleneck.subject,
        blocked.subject,
        excessive.subject,
        deficient.subject,
        missing.subject,
    }
    assigned.discard("")
    flows = _flows(active)
    flow_quality = flows[0].quality if flows else (
        FlowQuality.UNRESOLVED if not active else FlowQuality.FUNCTIONAL
    )
    if bottleneck.state is _ASSIGNED and flow_quality is FlowQuality.STRONG:
        flow_quality = FlowQuality.RESTRICTED
    if flow_quality is FlowQuality.EXCELLENT:
        flow_quality = FlowQuality.STRONG
    eco_state = _ecosystem_state(driver, bottleneck, blocked, flow_quality, mc01_bound)
    traces = (
        "TR-P7-ECO-DRIVER",
        "TR-P7-ECO-BOTTLENECK",
        "TR-P7-ECO-FLOW",
    )
    return TenGodEcosystemResult(
        analysis_id=natal.analysis_id,
        state=EvaluationStatus.PARTIALLY_RESOLVED if not mc01_bound else EvaluationStatus.RESOLVED,
        driver=driver,
        support=support,
        suppressed=suppressed,
        blocked=blocked,
        excessive=excessive,
        deficient=deficient,
        missing=missing,
        bottleneck=bottleneck,
        balancer=balancer,
        neutral=_neutral(natal, assigned),
        family_balances=_family_balances(index),
        flow=flows,
        flow_quality=flow_quality,
        ecosystem_state=eco_state,
        evidence_ids=natal.evidence_ids + combinations.evidence_ids,
        trace_ids=traces,
        confidence=ConfidenceValue(summary="low" if not mc01_bound else "moderate"),
    )
