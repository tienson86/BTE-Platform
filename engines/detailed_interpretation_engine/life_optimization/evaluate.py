"""Turn frozen findings into natal and temporal actions. Does not create truth."""

from __future__ import annotations

from engines.detailed_interpretation_engine.constants import LIFE_OPTIMIZATION_RULESET_VERSION, SCHEMA_LIFE_OPTIMIZATION
from engines.detailed_interpretation_engine.domains import DomainInterpretationResult
from engines.detailed_interpretation_engine.domain_interpretation.constants import HIGH_BANDS, LOW_BANDS
from engines.detailed_interpretation_engine.enums import (
    ActivationState,
    DomainState,
    EvaluationStatus,
    PriorityTier,
)
from engines.detailed_interpretation_engine.evidence_priority.constants import (
    SHEN_SHA_SOURCE_KINDS,
    SHEN_SHA_TIER_CEILING,
    TIER_INDEX,
)
from engines.detailed_interpretation_engine.life_optimization.constants import (
    CATEGORY_RANK,
    CONVERSION_BRIDGES,
    ELEMENT_FUNCTIONS,
    MAIN_OPTIMIZATION_IDS,
    SATURATION_STATES,
)
from engines.detailed_interpretation_engine.life_optimization.facts import (
    LifeOptimizationFacts,
    natal_evaluated,
)
from engines.detailed_interpretation_engine.life_optimization.models import (
    ActionContraindication,
    DomainConversionEfficiency,
    DomainOptimizationPlan,
    FiveElementOptimizationPlan,
    NatalOptimizationPlan,
    OptimizationAction,
    OptimizationConflict,
    OptimizationSaturation,
    TemporalOptimizationPlan,
    UsefulGodOptimizationPlan,
)
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_OVERLOAD = {ActivationState.OVERLOADED, ActivationState.PEAK}


def evaluate_life_optimization(facts: LifeOptimizationFacts) -> LifeOptimizationResult:
    """Consume Pack 07 findings and emit natal vs temporal action plans."""
    if not natal_evaluated(facts):
        return LifeOptimizationResult(
            analysis_id=facts.analysis_id,
            ruleset_version=LIFE_OPTIMIZATION_RULESET_VERSION,
        )
    saturations = _saturations(facts)
    natal_actions = _natal_actions(facts, saturations)
    temporal_actions = _temporal_actions(facts, saturations)
    actions = natal_actions + temporal_actions
    ranked = _rank(actions)
    top = tuple(item.action_id for item in ranked[:3])
    conflicts = _conflicts(facts, natal_actions, temporal_actions)
    domain_plans = _domain_plans(facts, actions, saturations)
    useful = _useful_god_plan(facts, natal_actions)
    elements = _element_plans(facts)
    evidence = tuple(dict.fromkeys(item for row in actions for item in row.evidence_ids))
    traces = tuple(dict.fromkeys(item for row in actions for item in row.trace_ids))
    natal_ids = tuple(item.action_id for item in natal_actions)
    temporal_ids = tuple(item.action_id for item in temporal_actions)
    confidence = _confidence(actions)
    return LifeOptimizationResult(
        schema_version=SCHEMA_LIFE_OPTIMIZATION,
        analysis_id=facts.analysis_id,
        ruleset_version=LIFE_OPTIMIZATION_RULESET_VERSION,
        state=EvaluationStatus.RESOLVED,
        natal_plan=NatalOptimizationPlan(
            state=EvaluationStatus.RESOLVED,
            summary_key="natal_long_term",
            action_ids=natal_ids,
            trace_ids=("TR-P7-OPT-natal",),
        ),
        temporal_plan=TemporalOptimizationPlan(
            state=EvaluationStatus.RESOLVED if temporal_actions else EvaluationStatus.NOT_EVALUATED,
            summary_key="current_luck_annual" if temporal_actions else "not_evaluated",
            luck_window=facts.luck.time_window,
            annual_window=facts.temporal.time_window,
            time_window=facts.temporal.time_window or facts.luck.time_window,
            action_ids=temporal_ids,
            saturations=saturations,
            trace_ids=("TR-P7-OPT-temporal",),
        ),
        top_priorities=top,
        actions=actions,
        conflicts=conflicts,
        domain_plans=domain_plans,
        element_plan=elements,
        useful_god_plan=useful,
        saturations=saturations,
        conditions=tuple(dict.fromkeys(item for row in actions for item in row.conditions)),
        warnings=("no_medical_advice", "no_specific_investment", "no_guaranteed_outcome"),
        evidence_ids=evidence,
        trace_ids=traces + ("TR-P7-OPT",),
        confidence=confidence,
    )


def action_urgency(action: OptimizationAction) -> tuple[int, int, str]:
    """Lower tuple is more urgent. Consumes DI-07 floor; does not rerank it."""
    return (
        TIER_INDEX.get(action.priority, 99),
        CATEGORY_RANK.get(action.category, 50),
        action.action_id,
    )


def _natal_actions(
    facts: LifeOptimizationFacts,
    saturations: tuple[OptimizationSaturation, ...],
) -> tuple[OptimizationAction, ...]:
    items: list[OptimizationAction] = []
    for domain_id in MAIN_OPTIMIZATION_IDS:
        natal = facts.natal.get(domain_id)
        if natal is None or natal.state is DomainState.NOT_EVALUATED:
            continue
        items.extend(_domain_natal_actions(facts, natal, saturations))
    useful = _useful_god_action(facts)
    if useful is not None:
        items.append(useful)
    return tuple(items)


def _domain_natal_actions(
    facts: LifeOptimizationFacts,
    natal: DomainInterpretationResult,
    saturations: tuple[OptimizationSaturation, ...],
) -> tuple[OptimizationAction, ...]:
    domain_id = natal.domain_id
    dims = natal.dimensions
    items: list[OptimizationAction] = []
    if domain_id == "wealth":
        items.extend(_wealth_actions(facts, natal))
    elif domain_id == "career":
        items.extend(_career_natal_actions(facts, natal, saturations))
    elif domain_id == "authority":
        items.extend(_authority_natal_actions(facts, natal, saturations))
    elif domain_id == "relationship" and natal.leakage == "communication":
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.relationship.develop_communication",
                mechanism="communication",
                action_type="develop",
                reason_key="relationship.communication",
                effect="increase_communication_quality",
                category="bottleneck" if natal.bottleneck else "leakage",
            )
        )
    elif domain_id == "legacy" and natal.leakage == "transmission":
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.legacy.develop_transmission",
                mechanism="transmission",
                action_type="develop",
                reason_key="legacy.transmission",
                effect="support_transmission",
                category="leakage",
            )
        )
    elif domain_id == "vitality" and natal.leakage in {"recovery", "stress"}:
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.vitality.protect_recovery",
                mechanism="recovery",
                action_type="recover" if natal.leakage == "recovery" else "protect",
                reason_key="vitality.recovery",
                effect="protect_recovery",
                category="leakage",
                extra_conditions=("no_medical",),
            )
        )
    _ = dims
    return tuple(items)


def _wealth_actions(
    facts: LifeOptimizationFacts,
    natal: DomainInterpretationResult,
) -> tuple[OptimizationAction, ...]:
    dims = natal.dimensions
    items: list[OptimizationAction] = []
    volatility_high = dims.get("volatility") in HIGH_BANDS
    creation_high = dims.get("creation") in HIGH_BANDS
    creation_low = dims.get("creation") in LOW_BANDS
    commercial_low = dims.get("commercialization") in LOW_BANDS
    retention_low = dims.get("retention") in LOW_BANDS
    if volatility_high or natal.leakage == "retention" or retention_low:
        contra = []
        if volatility_high:
            contra.append(
                ActionContraindication("expansion", "expansion_when_volatility_high")
            )
        if retention_low:
            contra.append(
                ActionContraindication("expansion", "expansion_when_retention_weak")
            )
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.wealth.retain_capital_discipline",
                mechanism="capital_discipline",
                action_type="retain",
                reason_key="wealth.volatility_high" if volatility_high else "wealth.volatility_high",
                effect="stabilize_capital",
                category="leakage" if natal.leakage or volatility_high else "critical_risk",
                extra_conditions=("no_investment_picks",),
                contraindications=tuple(contra),
            )
        )
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.wealth.avoid_expansion",
                mechanism="expansion",
                action_type="avoid",
                reason_key="wealth.volatility_high",
                effect="reduce_leakage",
                category="leakage",
                state="avoid",
                extra_conditions=("no_investment_picks",),
            )
        )
    if commercial_low and (creation_high or not creation_low):
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.wealth.convert_commercialization",
                mechanism="commercialization",
                action_type="convert",
                reason_key="wealth.commercialization_gap",
                effect="improve_commercialization",
                category="bottleneck",
            )
        )
    elif commercial_low and creation_low:
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.wealth.convert_commercialization",
                mechanism="commercialization",
                action_type="convert",
                reason_key="wealth.commercialization_gap",
                effect="improve_commercialization",
                category="bottleneck",
            )
        )
    return tuple(items)


def _career_natal_actions(
    facts: LifeOptimizationFacts,
    natal: DomainInterpretationResult,
    saturations: tuple[OptimizationSaturation, ...],
) -> tuple[OptimizationAction, ...]:
    if _saturated(saturations, "career"):
        return ()
    items: list[OptimizationAction] = []
    dims = natal.dimensions
    if natal.bottleneck in {"management", "management_gap"} or natal.risk == "management_gap":
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.career.support_management",
                mechanism="management",
                action_type="support",
                reason_key="career.management_gap",
                effect="support_management",
                category="bottleneck",
                contraindications=(
                    ActionContraindication("expansion", "expansion_when_management_weak"),
                ),
            )
        )
    technical_high = dims.get("technical_fit") in HIGH_BANDS or dims.get("academic_fit") in HIGH_BANDS
    role_low = dims.get("public_facing_fit") in LOW_BANDS or dims.get("entrepreneurial_fit") in LOW_BANDS
    if technical_high and role_low:
        items.append(
            _action(
                facts,
                natal,
                action_id="opt.career.convert_skill_to_role",
                mechanism="commercialization",
                action_type="convert",
                reason_key="career.skill_role_gap",
                effect="convert_skill_to_role",
                category="bottleneck",
            )
        )
    return tuple(items)


def _authority_natal_actions(
    facts: LifeOptimizationFacts,
    natal: DomainInterpretationResult,
    saturations: tuple[OptimizationSaturation, ...],
) -> tuple[OptimizationAction, ...]:
    if _saturated(saturations, "authority"):
        return ()
    if natal.dimensions.get("authority_pressure") == "elevated":
        return (
            _action(
                facts,
                natal,
                action_id="opt.authority.protect_pressure",
                mechanism="pressure_control",
                action_type="protect",
                reason_key="authority.overloaded",
                effect="control_authority_pressure",
                category="critical_risk",
            ),
        )
    return ()


def _temporal_actions(
    facts: LifeOptimizationFacts,
    saturations: tuple[OptimizationSaturation, ...],
) -> tuple[OptimizationAction, ...]:
    if facts.luck.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return ()
    items: list[OptimizationAction] = []
    for row in saturations:
        natal = facts.natal.get(row.domain)
        if natal is None:
            continue
        if row.domain == "career":
            items.append(
                _action(
                    facts,
                    natal,
                    action_id="opt.career.protect_workload",
                    mechanism="workload_control",
                    action_type="protect",
                    reason_key="career.overloaded",
                    effect="control_workload",
                    category="saturation",
                    time_scope="current_luck_cycle" if row.layer != "annual" else "current_annual",
                    extra_conditions=("more_workload_when_overloaded",),
                )
            )
            items.append(
                _action(
                    facts,
                    natal,
                    action_id="opt.career.avoid_expansion",
                    mechanism="workload_control",
                    action_type="avoid",
                    reason_key="career.overloaded",
                    effect="control_workload",
                    category="saturation",
                    time_scope="current_luck_cycle" if row.layer != "annual" else "current_annual",
                    state="avoid",
                )
            )
        if row.domain == "authority":
            items.append(
                _action(
                    facts,
                    natal,
                    action_id="opt.authority.protect_pressure",
                    mechanism="pressure_control",
                    action_type="protect",
                    reason_key="authority.overloaded",
                    effect="control_authority_pressure",
                    category="saturation",
                    time_scope="current_luck_cycle" if row.layer != "annual" else "current_annual",
                    extra_conditions=("more_authority_when_overloaded",),
                )
            )
            items.append(
                _action(
                    facts,
                    natal,
                    action_id="opt.authority.avoid_exposure",
                    mechanism="authority_exposure",
                    action_type="avoid",
                    reason_key="authority.overloaded",
                    effect="control_authority_pressure",
                    category="saturation",
                    time_scope="current_luck_cycle" if row.layer != "annual" else "current_annual",
                    state="avoid",
                )
            )
    vitality = facts.natal.get("vitality")
    if vitality is not None and _has_stress_transfer(facts, "career", "vitality"):
        items.append(
            _action(
                facts,
                vitality,
                action_id="opt.vitality.recover_capacity",
                mechanism="recovery",
                action_type="recover",
                reason_key="vitality.stress_from_career",
                effect="protect_recovery",
                category="critical_risk",
                time_scope="current_luck_cycle",
                extra_conditions=("no_medical",),
            )
        )
    return tuple(_unique(items))


def _useful_god_action(facts: LifeOptimizationFacts) -> OptimizationAction | None:
    if not facts.useful_element:
        return None
    natal = next((facts.natal[item] for item in MAIN_OPTIMIZATION_IDS if item in facts.natal), None)
    if natal is None:
        return None
    return _action(
        facts,
        natal,
        action_id="opt.element.support_function",
        mechanism="useful_god_function",
        action_type="support",
        reason_key="useful_god.function",
        effect="support_element_function",
        category="useful_god",
        domain_id="career" if "career" in facts.natal else natal.domain_id,
        extra_conditions=("function_first_element",),
    )


def _saturations(facts: LifeOptimizationFacts) -> tuple[OptimizationSaturation, ...]:
    items: list[OptimizationSaturation] = []
    for domain_id in MAIN_OPTIMIZATION_IDS:
        luck_item = facts.luck.items.get(domain_id)
        if luck_item is not None and luck_item.activation_state in _OVERLOAD:
            items.append(
                OptimizationSaturation(domain=domain_id, layer="luck_cycle", state="overloaded")
            )
        annual = facts.temporal.domain_results.get(domain_id)
        if annual is not None and annual.annual_expression_state in SATURATION_STATES:
            items.append(
                OptimizationSaturation(domain=domain_id, layer="annual", state="overloaded")
            )
    return tuple(items)


def _conflicts(
    facts: LifeOptimizationFacts,
    natal_actions: tuple[OptimizationAction, ...],
    temporal_actions: tuple[OptimizationAction, ...],
) -> tuple[OptimizationConflict, ...]:
    _ = natal_actions
    items: list[OptimizationConflict] = []
    by_id = {item.action_id: item for item in natal_actions + temporal_actions}
    if _has_stress_transfer(facts, "career", "vitality"):
        items.append(
            OptimizationConflict(
                conflict_id="opt.conflict.career_vitality_stress",
                action_a=by_id.get("opt.career.protect_workload", OptimizationAction()).action_id
                or "opt.career.protect_workload",
                action_b=by_id.get("opt.vitality.recover_capacity", OptimizationAction()).action_id
                or "opt.vitality.protect_recovery",
                domains=("career", "vitality"),
                severity="high",
                resolution_mode="conditional_balance",
                conditions=("do_not_silently_choose",),
                evidence_ids=_interaction_evidence(facts, "career", "vitality"),
                trace_ids=("TR-P7-OPT-conflict-cv",),
            )
        )
    for finding in facts.interaction.findings:
        if finding.interaction_type != "conflict":
            continue
        pair = tuple(sorted((finding.source_domain, finding.target_domain)))
        if pair != ("career", "wealth"):
            continue
        items.append(
            OptimizationConflict(
                conflict_id="opt.conflict.career_wealth",
                action_a="opt.career.protect_workload",
                action_b="opt.wealth.retain_capital_discipline",
                domains=pair,
                severity=finding.strength or "moderate",
                resolution_mode="conditional_balance",
                evidence_ids=finding.evidence_ids,
                trace_ids=finding.trace_ids + ("TR-P7-OPT-conflict-cw",),
            )
        )
    return tuple(items)


def _domain_plans(
    facts: LifeOptimizationFacts,
    actions: tuple[OptimizationAction, ...],
    saturations: tuple[OptimizationSaturation, ...],
) -> dict[str, DomainOptimizationPlan]:
    plans: dict[str, DomainOptimizationPlan] = {}
    for domain_id in MAIN_OPTIMIZATION_IDS:
        natal = facts.natal.get(domain_id)
        if natal is None or natal.state is DomainState.NOT_EVALUATED:
            plans[domain_id] = DomainOptimizationPlan(domain=domain_id)
            continue
        scoped = tuple(item for item in actions if item.target_domain == domain_id)
        recommended = tuple(
            item.action_id
            for item in scoped
            if item.time_scope == "natal_long_term"
            and item.action_type not in {"avoid", "monitor"}
            and item.category != "useful_god"
        )
        avoid = tuple(item.action_id for item in scoped if item.action_type == "avoid")
        if _saturated(saturations, domain_id):
            if domain_id == "career":
                avoid = tuple(dict.fromkeys(avoid + ("opt.career.strengthen_workload",)))
            if domain_id == "authority":
                avoid = tuple(dict.fromkeys(avoid + ("opt.authority.increase_exposure",)))
        temporal = tuple(
            item.action_id for item in scoped if item.time_scope != "natal_long_term"
        )
        plans[domain_id] = DomainOptimizationPlan(
            domain=domain_id,
            driver=natal.driver,
            bottleneck=natal.bottleneck,
            leakage=natal.leakage,
            conversion_efficiency=_conversion(natal),
            priority=_floor(facts, natal),
            recommended_actions=recommended,
            avoid_actions=avoid,
            conditions=natal.conditions,
            temporal_adjustments=temporal,
            confidence=natal.confidence,
            trace_ids=natal.trace_ids + (f"TR-P7-OPT-{domain_id}",),
            state=EvaluationStatus.RESOLVED,
        )
    return plans


def _useful_god_plan(
    facts: LifeOptimizationFacts,
    natal_actions: tuple[OptimizationAction, ...],
) -> UsefulGodOptimizationPlan:
    functions = ELEMENT_FUNCTIONS.get(facts.useful_element, ())
    action_ids = tuple(
        item.action_id for item in natal_actions if item.category == "useful_god"
    )
    return UsefulGodOptimizationPlan(
        useful_god=facts.useful_god or facts.useful_element,
        supporting_gods=facts.supporting_gods,
        avoidance_context=facts.ky_context,
        functional_targets=functions,
        domain_mappings=("career", "authority", "wealth") if functions else (),
        actions=action_ids,
        conditions=("function_first_element", "ky_is_not_total_ban"),
        confidence=ConfidenceValue(value=0.62, summary="life_optimization"),
        trace_ids=("TR-P7-OPT-useful-god",),
    )


def _element_plans(facts: LifeOptimizationFacts) -> tuple[FiveElementOptimizationPlan, ...]:
    items: list[FiveElementOptimizationPlan] = []
    if facts.useful_element:
        items.append(
            FiveElementOptimizationPlan(
                element=facts.useful_element,
                current_role="useful_god",
                desired_role="functional_support",
                action_direction="support",
                target_domains=("career", "authority", "wealth"),
                conditions=("function_first_element", "not_raw_element_count"),
                confidence=ConfidenceValue(value=0.62, summary="life_optimization"),
                trace_ids=("TR-P7-OPT-element",),
            )
        )
    for token in facts.ky_context:
        element = next((item for item in ELEMENT_FUNCTIONS if item in token), "")
        if not element or (facts.useful_element and element == facts.useful_element):
            continue
        items.append(
            FiveElementOptimizationPlan(
                element=element,
                current_role="ky_context",
                desired_role="avoid_reinforcing",
                action_direction="reduce",
                target_domains=(),
                conditions=("ky_is_not_total_ban",),
                contraindications=(
                    ActionContraindication("total_ban", "ky.not_ban", "caution"),
                ),
                confidence=ConfidenceValue(value=0.55, summary="life_optimization"),
                trace_ids=("TR-P7-OPT-element-ky",),
            )
        )
    return tuple(items)


def _conversion(natal: DomainInterpretationResult) -> DomainConversionEfficiency:
    bridge = CONVERSION_BRIDGES.get(natal.domain_id, ("", ""))
    dims = natal.dimensions
    efficiency = "unresolved"
    bottleneck = natal.bottleneck
    if natal.domain_id == "wealth":
        if dims.get("creation") in HIGH_BANDS and dims.get("commercialization") in LOW_BANDS:
            efficiency = "low"
            bottleneck = "commercialization"
        elif dims.get("volatility") in HIGH_BANDS:
            efficiency = "low"
            bottleneck = bottleneck or "capital_discipline"
        elif dims.get("retention") in HIGH_BANDS:
            efficiency = "moderate"
    elif natal.domain_id == "career":
        technical = dims.get("technical_fit") in HIGH_BANDS or dims.get("academic_fit") in HIGH_BANDS
        role = dims.get("public_facing_fit") in LOW_BANDS or dims.get("entrepreneurial_fit") in LOW_BANDS
        if technical and role:
            efficiency = "low"
            bottleneck = "skill_to_role"
    elif natal.leakage:
        efficiency = "low"
        bottleneck = natal.leakage
    return DomainConversionEfficiency(
        domain=natal.domain_id,
        from_capability=bridge[0],
        to_expression=bridge[1],
        efficiency=efficiency,
        bottleneck=bottleneck,
    )


def _action(
    facts: LifeOptimizationFacts,
    natal: DomainInterpretationResult,
    *,
    action_id: str,
    mechanism: str,
    action_type: str,
    reason_key: str,
    effect: str,
    category: str,
    time_scope: str = "natal_long_term",
    state: str = "recommended",
    extra_conditions: tuple[str, ...] = (),
    contraindications: tuple[ActionContraindication, ...] = (),
    domain_id: str = "",
) -> OptimizationAction:
    target = domain_id or natal.domain_id
    floor = _floor(facts, natal if natal.domain_id == target else facts.natal.get(target, natal))
    if category == "shen_sha":
        floor = _ceil(floor, SHEN_SHA_TIER_CEILING.value)
        state = "monitor"
        action_type = "monitor"
    return OptimizationAction(
        action_id=action_id if time_scope == "natal_long_term" else f"{action_id}.{time_scope}",
        target_domain=target,
        target_mechanism=mechanism,
        action_type=action_type,
        priority=floor,
        recommended_action_key=action_id,
        reason_key=reason_key,
        conditions=tuple(dict.fromkeys(natal.conditions + extra_conditions)),
        contraindications=contraindications,
        time_scope=time_scope,
        expected_structural_effect=effect,
        evidence_ids=natal.evidence_ids or facts.evidence_priority.evidence_ids[:1] or (f"E-OPT-{target}",),
        trace_ids=natal.trace_ids + (f"TR-P7-OPT-{target}",),
        confidence=natal.confidence if natal.confidence.value is not None else ConfidenceValue(
            value=0.64, summary="life_optimization"
        ),
        state=state,
        category=category,
        driver_kind="useful_god" if category == "useful_god" else "domain",
    )


def _floor(facts: LifeOptimizationFacts, natal: DomainInterpretationResult) -> str:
    ranks: list[str] = []
    for finding in facts.evidence_priority.findings:
        if finding.source_kind in SHEN_SHA_SOURCE_KINDS:
            continue
        if finding.domain != natal.domain_id and finding.domain not in {natal.domain_id}:
            continue
        if finding.tier is PriorityTier.P5:
            continue
        ranks.append(finding.tier.value)
    if natal.priority in TIER_INDEX:
        ranks.append(natal.priority)
    if not ranks:
        return "P2"
    return min(ranks, key=lambda item: TIER_INDEX.get(item, 99))


def _ceil(current: str, ceiling: str) -> str:
    if TIER_INDEX.get(current, 99) < TIER_INDEX.get(ceiling, 99):
        return ceiling
    return current


def _rank(actions: tuple[OptimizationAction, ...]) -> tuple[OptimizationAction, ...]:
    drivers = [item for item in actions if item.driver_kind != "shen_sha" and item.priority != "P5"]
    seen: set[str] = set()
    ordered: list[OptimizationAction] = []
    for item in sorted(drivers, key=action_urgency):
        key = item.recommended_action_key or item.action_id
        if key in seen or item.action_type == "avoid":
            continue
        seen.add(key)
        ordered.append(item)
    return tuple(ordered)


def _saturated(rows: tuple[OptimizationSaturation, ...], domain_id: str) -> bool:
    return any(item.domain == domain_id for item in rows)


def _has_stress_transfer(facts: LifeOptimizationFacts, source: str, target: str) -> bool:
    for finding in facts.interaction.findings:
        if finding.interaction_type != "stress_transfer":
            continue
        if finding.source_domain == source and finding.target_domain == target:
            return True
    for item in facts.interaction.stress_transfers:
        if item.source_domain == source and item.target_domain == target:
            return True
    return False


def _interaction_evidence(facts: LifeOptimizationFacts, source: str, target: str) -> tuple[str, ...]:
    for finding in facts.interaction.findings:
        if finding.source_domain == source and finding.target_domain == target:
            return finding.evidence_ids
    return facts.interaction.evidence_ids


def _unique(items: list[OptimizationAction]) -> list[OptimizationAction]:
    seen: set[str] = set()
    unique: list[OptimizationAction] = []
    for item in items:
        if item.action_id in seen:
            continue
        seen.add(item.action_id)
        unique.append(item)
    return unique


def _confidence(actions: tuple[OptimizationAction, ...]) -> ConfidenceValue:
    values = [item.confidence.value for item in actions if item.confidence.value is not None]
    if not values:
        return ConfidenceValue(value=0.64, summary="life_optimization")
    return ConfidenceValue(value=round(min(values), 2), summary="life_optimization")
