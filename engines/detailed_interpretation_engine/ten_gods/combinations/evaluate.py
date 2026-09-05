"""Evaluate V1 Ten God combinations. Co-presence is never proof."""

from __future__ import annotations

from dataclasses import dataclass, replace

from engines.detailed_interpretation_engine.enums import (
    ChainQuality,
    CombinationReach,
    CombinationRelativePower,
    CombinationState,
    CombinationStructuralRole,
    DayMasterBand,
    TenGodConfidenceBand,
    TenGodUsefulGodContext,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.constants import (
    CONDITION_DAY_MASTER_MISMATCH,
    CONDITION_MC01_NOT_BOUND,
    CONDITION_MEDIATED_REACH,
    CONDITION_RESIDUAL_ONLY,
    CONDITION_UNRESOLVED_DEPENDENCY,
    CombinationSpec,
    POSITIVE_CODES,
    RISK_CODES,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.helpers import (
    as_participant,
    best_member,
    carrier_participant,
    dm_matches,
    family_items,
    generation_state,
    is_material,
    is_present,
    is_residual_only,
    meets_min_strength,
    natal_index,
    pattern_of,
    quality_from_ranks,
    rank_of,
    relative_power,
    structural_role_for,
    two_node_chain,
    useful_of,
)
from engines.detailed_interpretation_engine.ten_gods.combinations.models import (
    TenGodChainFinding,
    TenGodChainLink,
    TenGodCombinationResult,
)
from engines.detailed_interpretation_engine.ten_gods.models import (
    TenGodInterpretationCollection,
    TenGodInterpretationResult,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


@dataclass(frozen=True, slots=True)
class Mc01ComboRefs:
    """Consumed MC-01 structural IDs. Pack 07 does not create them."""

    bound: bool = False
    damage_ids: tuple[str, ...] = ()
    rescue_ids: tuple[str, ...] = ()
    purity_ref: str = ""

    def ids_for(self, spec: CombinationSpec) -> tuple[str, ...]:
        """Return canonical MC-01 IDs required by this combination, if any."""
        if spec.requires_mc01 == "damage":
            return self.damage_ids
        if spec.requires_mc01 == "rescue":
            return self.rescue_ids
        if spec.requires_mc01 == "purity" and self.purity_ref.strip():
            return (self.purity_ref.strip(),)
        return ()

    def requirement_met(self, spec: CombinationSpec) -> bool:
        """True when this spec has no MC-01 ID gate, or those IDs exist."""
        if spec.requires_mc01 in {"", "optional"}:
            return True
        return bool(self.ids_for(spec))


def _confidence(*items: TenGodInterpretationResult | None, mc01_bound: bool) -> ConfidenceValue:
    if not mc01_bound:
        return ConfidenceValue(summary=TenGodConfidenceBand.LOW.value)
    if any(item is None or item.useful_god_context is TenGodUsefulGodContext.UNRESOLVED for item in items):
        return ConfidenceValue(summary=TenGodConfidenceBand.MODERATE.value)
    return ConfidenceValue(summary=TenGodConfidenceBand.MODERATE.value)


def _inactive(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    *,
    source: str = "",
    target: str = "",
    conditions: tuple[str, ...] = (),
    participants: tuple = (),
    chain: TenGodChainFinding | None = None,
    quality: ChainQuality = ChainQuality.UNRESOLVED,
    power: CombinationRelativePower = CombinationRelativePower.UNCERTAIN,
) -> TenGodCombinationResult:
    dm = natal.items[0].day_master_context if natal.items else DayMasterBand.UNRESOLVED
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=CombinationState.INACTIVE,
        participants=participants,
        source=source,
        target=target,
        relationship=spec.kind,
        relative_power=power,
        chain=chain or TenGodChainFinding(chain_id=f"CH-{spec.combination_id}"),
        chain_quality=quality,
        structural_role=CombinationStructuralRole.INCIDENTAL_RELATION,
        day_master_context=dm,
        pattern_context=pattern_of(*natal.items[:1]),
        causal_group=spec.causal_group,
        conditions=conditions,
        evidence_ids=(),
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=ConfidenceValue(summary=TenGodConfidenceBand.LOW.value),
    )


def _pick(
    spec: CombinationSpec,
    index: dict[str, TenGodInterpretationResult],
    *,
    material_only: bool = False,
) -> tuple[TenGodInterpretationResult | None, TenGodInterpretationResult | None]:
    source = index.get(spec.source_god) if spec.source_god else best_member(
        family_items(index, spec.source_family), material_only=material_only
    )
    target = index.get(spec.target_god) if spec.target_god else best_member(
        family_items(index, spec.target_family), material_only=material_only
    )
    if spec.source_god:
        source = index.get(spec.source_god)
    if spec.target_god:
        target = index.get(spec.target_god)
    return source, target


def _generation(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
) -> TenGodCombinationResult:
    source, target = _pick(spec, index)
    if not is_present(source) or not is_present(target) or source is None or target is None:
        if is_present(source) ^ is_present(target):
            present = source if is_present(source) else target
            missing_role = "target" if is_present(source) else "source"
            quality = ChainQuality.BROKEN
            chain = TenGodChainFinding(
                chain_id=f"CH-{spec.combination_id}",
                nodes=(source.ten_god_id if source and is_present(source) else spec.source_family,
                       target.ten_god_id if target and is_present(target) else spec.target_family),
                quality=quality,
                weakest_link=missing_role,
                broken_link_ids=(f"{missing_role}-missing",),
            )
            return TenGodCombinationResult(
                combination_id=spec.combination_id,
                combination_type=spec.types,
                state=CombinationState.BROKEN,
                participants=tuple(
                    as_participant(item, role)
                    for item, role in ((source, "source"), (target, "target"))
                    if item is not None and is_present(item)
                ),
                source=source.ten_god_id if source and is_present(source) else "",
                target=target.ten_god_id if target and is_present(target) else "",
                relationship="generates",
                chain=chain,
                chain_quality=quality,
                day_master_context=present.day_master_context if present else DayMasterBand.UNRESOLVED,
                pattern_context=pattern_of(source, target),
                causal_group=spec.causal_group,
                conditions=(CONDITION_RESIDUAL_ONLY,) if is_residual_only(source) or is_residual_only(target) else (),
                trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
                confidence=_confidence(source, target, mc01_bound=mc01_bound),
            )
        return _inactive(spec, natal)
    residual = is_residual_only(source) or is_residual_only(target) or not is_material(source)
    ranks = (rank_of(source) or 0, rank_of(target) or 0)
    quality = ChainQuality.UNRESOLVED if residual else quality_from_ranks(ranks)
    if residual:
        quality = ChainQuality.UNRESOLVED
    state = generation_state(quality, residual=residual)
    reach = CombinationReach.DIRECT if is_material(source) and is_material(target) else CombinationReach.CONDITIONAL
    link_state = "intact" if state is CombinationState.CONFIRMED else state.value
    chain = two_node_chain(
        f"CH-{spec.combination_id}", source, target, "generates", quality, reach, link_state
    )
    conditions: list[str] = []
    if residual:
        conditions.append(CONDITION_RESIDUAL_ONLY)
    if not mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    positives = POSITIVE_CODES.get(spec.combination_id, ()) if state in {
        CombinationState.CONFIRMED, CombinationState.CONDITIONAL, CombinationState.WEAK
    } else ()
    risks = RISK_CODES.get(spec.combination_id, ())[:1] if state is CombinationState.WEAK else ()
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=state,
        participants=(as_participant(source, "source"), as_participant(target, "target")),
        source=source.ten_god_id,
        target=target.ten_god_id,
        relationship="generates",
        relative_power=relative_power(source, target),
        chain=chain,
        chain_quality=quality,
        structural_role=structural_role_for((source, target), state),
        day_master_context=source.day_master_context,
        pattern_context=pattern_of(source, target),
        useful_god_context=useful_of(source, target),
        positive_expressions=positives,
        risk_expressions=risks,
        conditions=tuple(conditions),
        causal_group=spec.causal_group,
        evidence_ids=source.evidence_ids + target.evidence_ids,
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=_confidence(source, target, mc01_bound=mc01_bound),
    )


def _three_node_chain(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
) -> TenGodCombinationResult:
    nodes = tuple(best_member(family_items(index, family)) for family in spec.chain_families)
    present = tuple(node for node in nodes if node is not None and is_present(node))
    if len(present) < 2:
        return _inactive(spec, natal)
    ranks = tuple((rank_of(node) or 0) if node is not None and is_present(node) else 0 for node in nodes)
    missing = [family for family, node in zip(spec.chain_families, nodes) if not is_present(node)]
    residual = any(node is not None and is_residual_only(node) for node in nodes)
    if missing or residual:
        quality = ChainQuality.BROKEN if missing else ChainQuality.UNRESOLVED
        state = CombinationState.BROKEN if missing else CombinationState.INACTIVE
        conditions = (CONDITION_RESIDUAL_ONLY,) if residual and not missing else ()
        links = []
        for left, right, family_left, family_right in zip(
            nodes, nodes[1:], spec.chain_families, spec.chain_families[1:]
        ):
            links.append(
                TenGodChainLink(
                    source=left.ten_god_id if left and is_present(left) else family_left,
                    target=right.ten_god_id if right and is_present(right) else family_right,
                    vector="generates",
                    reach=CombinationReach.DIRECT,
                    state="broken" if not is_present(left) or not is_present(right) else "weak",
                )
            )
        chain = TenGodChainFinding(
            chain_id=f"CH-{spec.combination_id}",
            nodes=tuple(
                node.ten_god_id if node and is_present(node) else family
                for node, family in zip(nodes, spec.chain_families)
            ),
            links=tuple(links),
            quality=quality,
            weakest_link=missing[0] if missing else spec.chain_families[1],
            broken_link_ids=tuple(f"{name}-missing" for name in missing),
        )
        if quality is ChainQuality.BROKEN and state is CombinationState.BROKEN:
            assert quality is not ChainQuality.STRONG
        return TenGodCombinationResult(
            combination_id=spec.combination_id,
            combination_type=spec.types,
            state=state,
            participants=tuple(as_participant(item, "node") for item in present),
            source=present[0].ten_god_id,
            target=present[-1].ten_god_id,
            mediator=present[1].ten_god_id if len(present) > 2 else (nodes[1].ten_god_id if nodes[1] and is_present(nodes[1]) else ""),
            relationship="generates",
            chain=chain,
            chain_quality=quality,
            day_master_context=present[0].day_master_context,
            pattern_context=pattern_of(*present),
            conditions=conditions + ((CONDITION_MC01_NOT_BOUND,) if not mc01_bound else ()),
            causal_group=spec.causal_group,
            evidence_ids=tuple(eid for item in present for eid in item.evidence_ids),
            trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
            confidence=_confidence(*present, mc01_bound=mc01_bound),
        )
    first, mid, last = nodes[0], nodes[1], nodes[2]
    assert first is not None and mid is not None and last is not None
    quality = quality_from_ranks(ranks)
    state = generation_state(quality, residual=False)
    weakest_id = min((first, mid, last), key=lambda item: rank_of(item) or 0).ten_god_id
    chain = TenGodChainFinding(
        chain_id=f"CH-{spec.combination_id}",
        nodes=(first.ten_god_id, mid.ten_god_id, last.ten_god_id),
        links=(
            TenGodChainLink(first.ten_god_id, mid.ten_god_id, "generates", CombinationReach.DIRECT, "intact"),
            TenGodChainLink(mid.ten_god_id, last.ten_god_id, "generates", CombinationReach.DIRECT, "intact"),
        ),
        quality=quality,
        weakest_link=weakest_id,
    )
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=state,
        participants=(
            as_participant(first, "source"),
            as_participant(mid, "mediator"),
            as_participant(last, "target"),
        ),
        source=first.ten_god_id,
        target=last.ten_god_id,
        mediator=mid.ten_god_id,
        relationship="generates",
        relative_power=relative_power(first, last, mediated=True),
        chain=chain,
        chain_quality=quality,
        structural_role=structural_role_for((first, mid, last), state),
        day_master_context=first.day_master_context,
        pattern_context=pattern_of(first, mid, last),
        useful_god_context=useful_of(first, mid, last),
        positive_expressions=POSITIVE_CODES.get(spec.combination_id, ()) if state is CombinationState.CONFIRMED else (),
        conditions=(CONDITION_MC01_NOT_BOUND,) if not mc01_bound else (),
        causal_group=spec.causal_group,
        evidence_ids=first.evidence_ids + mid.evidence_ids + last.evidence_ids,
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=_confidence(first, mid, last, mc01_bound=mc01_bound),
    )


def _control_or_transform(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
    refs: Mc01ComboRefs,
) -> TenGodCombinationResult:
    source, target = _pick(spec, index)
    mediator = best_member(family_items(index, spec.mediation_family)) if spec.mediation_family else None
    if spec.kind == "transform":
        source = index.get(spec.source_god)
        target = best_member(family_items(index, spec.mediator_family))
        mediator = target
    if not is_present(source) or not is_present(target) or source is None or target is None:
        return _inactive(spec, natal)
    residual = is_residual_only(source) or is_residual_only(target) or not is_material(source)
    mediated = bool(
        spec.mediation_family
        and mediator is not None
        and is_material(mediator)
        and is_material(source)
        and is_material(target)
    )
    if residual:
        return _inactive(
            spec,
            natal,
            source=source.ten_god_id,
            target=target.ten_god_id,
            conditions=(CONDITION_RESIDUAL_ONLY,),
            participants=(as_participant(source, "source"), as_participant(target, "target")),
        )
    if mediated:
        assert mediator is not None
        return _inactive(
            spec,
            natal,
            source=source.ten_god_id,
            target=target.ten_god_id,
            conditions=(CONDITION_MEDIATED_REACH,),
            participants=(
                as_participant(source, "source"),
                as_participant(target, "target"),
                as_participant(mediator, "mediator"),
            ),
            power=CombinationRelativePower.MEDIATED,
        )
    conditions = []
    structural_ids = refs.ids_for(spec)
    if not refs.requirement_met(spec):
        conditions.append(CONDITION_UNRESOLVED_DEPENDENCY)
    if not mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    quality = quality_from_ranks((rank_of(source) or 0, rank_of(target) or 0))
    if quality is ChainQuality.STRONG and not structural_ids:
        quality = ChainQuality.CONDITIONAL
    if structural_ids:
        state = generation_state(quality, residual=False)
        role = structural_role_for((source, target), state)
        link_state = "intact" if state is CombinationState.CONFIRMED else "conditional"
        chain_quality = quality
    else:
        state = CombinationState.UNRESOLVED
        role = CombinationStructuralRole.UNRESOLVED
        link_state = "conditional"
        chain_quality = ChainQuality.CONDITIONAL
        if quality is ChainQuality.STRONG:
            quality = ChainQuality.CONDITIONAL
    chain = two_node_chain(
        f"CH-{spec.combination_id}",
        source,
        target,
        "transforms" if spec.kind == "transform" else "controls",
        chain_quality,
        CombinationReach.DIRECT,
        link_state,
    )
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=state,
        participants=(as_participant(source, "source"), as_participant(target, "target")),
        source=source.ten_god_id,
        target=target.ten_god_id,
        mediator=mediator.ten_god_id if mediator and is_present(mediator) and spec.kind == "transform" else "",
        relationship="transforms" if spec.kind == "transform" else "controls",
        relative_power=relative_power(source, target),
        chain=chain,
        chain_quality=chain_quality,
        structural_role=role,
        day_master_context=source.day_master_context,
        pattern_context=pattern_of(source, target),
        useful_god_context=useful_of(source, target),
        damage_ids=structural_ids if spec.requires_mc01 == "damage" else (),
        rescue_ids=structural_ids if spec.requires_mc01 == "rescue" else (),
        conditions=tuple(conditions),
        causal_group=spec.causal_group,
        evidence_ids=source.evidence_ids + target.evidence_ids,
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=ConfidenceValue(summary=TenGodConfidenceBand.LOW.value)
        if not structural_ids
        else _confidence(source, target, mc01_bound=mc01_bound),
    )


def _mixed(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
    refs: Mc01ComboRefs,
) -> TenGodCombinationResult:
    left, right = index.get(spec.source_god), index.get(spec.target_god)
    if not is_present(left) or not is_present(right) or left is None or right is None:
        return _inactive(spec, natal)
    if is_residual_only(left) or is_residual_only(right):
        return _inactive(
            spec,
            natal,
            source=left.ten_god_id,
            target=right.ten_god_id,
            conditions=(CONDITION_RESIDUAL_ONLY,),
        )
    structural_ids = refs.ids_for(spec)
    conditions = []
    if not refs.requirement_met(spec):
        conditions.append(CONDITION_UNRESOLVED_DEPENDENCY)
    if not mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    state = CombinationState.CONDITIONAL if structural_ids else CombinationState.UNRESOLVED
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=state,
        participants=(as_participant(left, "source"), as_participant(right, "target")),
        source=left.ten_god_id,
        target=right.ten_god_id,
        relationship="mixed",
        relative_power=relative_power(left, right),
        chain=TenGodChainFinding(chain_id=f"CH-{spec.combination_id}", nodes=(left.ten_god_id, right.ten_god_id)),
        chain_quality=ChainQuality.CONDITIONAL,
        day_master_context=left.day_master_context,
        pattern_context=pattern_of(left, right),
        damage_ids=(),
        conditions=tuple(conditions),
        causal_group=spec.causal_group,
        evidence_ids=left.evidence_ids + right.evidence_ids,
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=ConfidenceValue(summary=TenGodConfidenceBand.LOW.value)
        if not structural_ids
        else _confidence(left, right, mc01_bound=mc01_bound),
    )


def _capacity(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
    refs: Mc01ComboRefs,
) -> TenGodCombinationResult:
    force = index.get(spec.source_god) if spec.source_god else best_member(family_items(index, spec.source_family))
    dm = natal.items[0].day_master_context if natal.items else DayMasterBand.UNRESOLVED
    if not is_present(force) or force is None:
        return _inactive(spec, natal)
    if not dm_matches(dm, spec.dm_required):
        return _inactive(
            spec,
            natal,
            source=force.ten_god_id,
            target="day_master",
            conditions=(CONDITION_DAY_MASTER_MISMATCH,),
            participants=(as_participant(force, "source"), carrier_participant(dm)),
        )
    if not is_material(force) or not meets_min_strength(force, spec.min_strength):
        return _inactive(spec, natal, source=force.ten_god_id, target="day_master")
    optional = spec.requires_mc01 == "optional"
    structural_ids = refs.ids_for(spec)
    if optional:
        state = CombinationState.CONDITIONAL
    elif structural_ids:
        state = CombinationState.CONDITIONAL
    else:
        state = CombinationState.UNRESOLVED
    conditions = []
    if not optional and not refs.requirement_met(spec):
        conditions.append(CONDITION_UNRESOLVED_DEPENDENCY)
    if not mc01_bound:
        conditions.append(CONDITION_MC01_NOT_BOUND)
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=state,
        participants=(as_participant(force, "source"), carrier_participant(dm)),
        source=force.ten_god_id,
        target="day_master",
        relationship="capacity_mismatch",
        relative_power=CombinationRelativePower.SOURCE_DOMINANT
        if (rank_of(force) or 0) >= 4
        else CombinationRelativePower.BALANCED,
        chain=TenGodChainFinding(
            chain_id=f"CH-{spec.combination_id}",
            nodes=(force.ten_god_id, "day_master"),
            quality=ChainQuality.CONDITIONAL,
            weakest_link="day_master",
        ),
        chain_quality=ChainQuality.CONDITIONAL,
        day_master_context=dm,
        pattern_context=pattern_of(force),
        damage_ids=structural_ids if spec.requires_mc01 == "damage" else (),
        rescue_ids=structural_ids if spec.requires_mc01 == "rescue" else (),
        positive_expressions=POSITIVE_CODES.get(spec.combination_id, ())[:1],
        risk_expressions=RISK_CODES.get(spec.combination_id, ())[:1],
        conditions=tuple(conditions),
        causal_group=spec.causal_group,
        evidence_ids=force.evidence_ids,
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=ConfidenceValue(summary=TenGodConfidenceBand.LOW.value),
    )


def _use(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    index: dict[str, TenGodInterpretationResult],
    mc01_bound: bool,
) -> TenGodCombinationResult:
    target = best_member(family_items(index, spec.target_family), material_only=True)
    dm = natal.items[0].day_master_context if natal.items else DayMasterBand.UNRESOLVED
    if not dm_matches(dm, spec.dm_required):
        return _inactive(spec, natal, conditions=(CONDITION_DAY_MASTER_MISMATCH,))
    if target is None or not is_material(target):
        return _inactive(spec, natal)
    dm_rank = 2 if spec.dm_required == "weak" else 4
    quality = quality_from_ranks((dm_rank, rank_of(target) or 0))
    state = CombinationState.CONFIRMED if quality in {ChainQuality.FUNCTIONAL, ChainQuality.STRONG, ChainQuality.VERY_STRONG} else CombinationState.WEAK
    if target.useful_god_context is TenGodUsefulGodContext.UNFAVORABLE:
        state = CombinationState.CONDITIONAL
    conditions = [] if mc01_bound else [CONDITION_MC01_NOT_BOUND]
    return TenGodCombinationResult(
        combination_id=spec.combination_id,
        combination_type=spec.types,
        state=state,
        participants=(carrier_participant(dm), as_participant(target, "target")),
        source="day_master",
        target=target.ten_god_id,
        relationship="uses",
        relative_power=CombinationRelativePower.BALANCED,
        chain=TenGodChainFinding(
            chain_id=f"CH-{spec.combination_id}",
            nodes=("day_master", target.ten_god_id),
            links=(
                TenGodChainLink("day_master", target.ten_god_id, "uses", CombinationReach.DIRECT, "intact"),
            ),
            quality=quality,
            weakest_link=target.ten_god_id,
        ),
        chain_quality=quality,
        structural_role=structural_role_for((target,), state),
        day_master_context=dm,
        pattern_context=pattern_of(target),
        useful_god_context=target.useful_god_context,
        positive_expressions=POSITIVE_CODES.get(spec.combination_id, ()),
        risk_expressions=RISK_CODES.get(spec.combination_id, ())[:1],
        conditions=tuple(conditions),
        causal_group=spec.causal_group,
        evidence_ids=target.evidence_ids,
        trace_ids=(f"TR-P7-COMB-{spec.combination_id}",),
        confidence=_confidence(target, mc01_bound=mc01_bound),
    )


def evaluate_spec(
    spec: CombinationSpec,
    natal: TenGodInterpretationCollection,
    *,
    mc01_bound: bool,
    damage_ids: tuple[str, ...] = (),
    rescue_ids: tuple[str, ...] = (),
    purity_ref: str = "",
) -> TenGodCombinationResult:
    """Evaluate one V1 combination from DI-01 profiles."""
    index = natal_index(natal.items)
    refs = Mc01ComboRefs(
        bound=mc01_bound,
        damage_ids=damage_ids,
        rescue_ids=rescue_ids,
        purity_ref=purity_ref,
    )
    if spec.kind == "generation":
        return _generation(spec, natal, index, mc01_bound)
    if spec.kind == "chain":
        return _three_node_chain(spec, natal, index, mc01_bound)
    if spec.kind in {"control", "transform"}:
        return _control_or_transform(spec, natal, index, mc01_bound, refs)
    if spec.kind == "mixed":
        return _mixed(spec, natal, index, mc01_bound, refs)
    if spec.kind == "capacity":
        return _capacity(spec, natal, index, mc01_bound, refs)
    return _use(spec, natal, index, mc01_bound)


def apply_chain_dedupe(
    items: tuple[TenGodCombinationResult, ...],
) -> tuple[TenGodCombinationResult, ...]:
    """Keep one causal chain. Do not emit three findings for Tài→Quan→Ấn."""
    by_id = {item.combination_id: item for item in items}
    three = by_id.get("wealth_officer_resource_chain")
    if three is None or three.state not in {
        CombinationState.CONFIRMED,
        CombinationState.CONDITIONAL,
        CombinationState.WEAK,
    }:
        return items
    tagged: list[TenGodCombinationResult] = []
    for item in items:
        if item.combination_id in {"wealth_generates_officer", "officer_generates_resource"}:
            tagged.append(
                replace(
                    item,
                    source_combination_id=three.combination_id,
                    source_chain_id=three.chain.chain_id,
                )
            )
        else:
            tagged.append(item)
    return tuple(tagged)
