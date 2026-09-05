"""Evaluate annual expression inside the luck envelope. Does not rewrite natal or luck."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domains import DomainInterpretationResult
from engines.detailed_interpretation_engine.enums import ActivationState, DomainState, EvaluationStatus
from engines.detailed_interpretation_engine.luck_activation.constants import (
    DOMAIN_STRESS_FAMILIES,
    DOMAIN_SUPPORT_FAMILIES,
    LEVEL_RANK,
    MAIN_ACTIVATION_IDS,
    NATAL_LIMITED,
    NATAL_MISSING,
    NATAL_STRONG,
    OVERLOAD_DOMAINS,
)
from engines.detailed_interpretation_engine.luck_activation.models import DomainActivationResult
from engines.detailed_interpretation_engine.temporal import LuckActivationResult
from engines.detailed_interpretation_engine.temporal_activation.constants import (
    EXPRESSION_RANK,
    GOD_TO_ANNUAL_DRIVER,
    LEVELS,
    MAIN_TEMPORAL_IDS,
    TEMPORAL_DRIVER_IDS,
)
from engines.detailed_interpretation_engine.temporal_activation.facts import TemporalActivationContext
from engines.detailed_interpretation_engine.temporal_activation.labels import BOTTLENECK_LABELS
from engines.detailed_interpretation_engine.temporal_activation.models import (
    ActivationEnvelope,
    TemporalActivationModifier,
    TemporalDomainActivationResult,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def evaluate_annual_domains(
    facts: TemporalActivationContext,
) -> dict[str, TemporalDomainActivationResult]:
    """Build one annual expression object per published domain."""
    order = _order(facts)
    return {domain_id: evaluate_annual_domain(domain_id, facts) for domain_id in order}


def evaluate_annual_domain(
    domain_id: str,
    facts: TemporalActivationContext,
) -> TemporalDomainActivationResult:
    """Refine luck-window expression for one domain. Does not overwrite luck state."""
    natal = facts.natal.get(domain_id)
    luck_item = facts.luck_cycle_result.items.get(domain_id)
    parent_state = _parent_state(luck_item)
    natal_state = natal.state.value if natal is not None else ""
    if natal is None or luck_item is None:
        return _empty(domain_id, parent_state, natal_state)
    if natal.state in {DomainState.NOT_EVALUATED, DomainState.UNRESOLVED}:
        return _copy_parent(natal, luck_item, "stabilize", "unresolved", "none", "none", "none")
    if natal.state is DomainState.BLOCKED or luck_item.activation_state is ActivationState.BLOCKED:
        return _copy_parent(natal, luck_item, "stabilize", "blocked", "none", "none", "none")
    family = facts.annual.family if facts.annual is not None else ""
    support_rank, stress_rank = _ranks(domain_id, family, facts)
    support_rank, stress_rank, relation_notes = _relation_guard(
        domain_id,
        family,
        support_rank,
        stress_rank,
        facts,
        natal,
        luck_item,
    )
    effect = _modifier_effect(domain_id, family, support_rank, stress_rank, parent_state, natal_state)
    overloaded = _overloaded(domain_id, natal_state, parent_state, support_rank, effect)
    expression = _expression(parent_state, effect, support_rank, natal_state, overloaded)
    driver_id = _driver_id(expression, effect, facts)
    bottleneck = _bottleneck(domain_id, family, parent_state, expression, stress_rank)
    support = _level(support_rank if not overloaded else max(support_rank, 4))
    stress = _level(stress_rank if expression != "overloaded" else max(stress_rank, 3))
    recovery = _recovery_level(effect, expression)
    conditions = _conditions(
        natal_state,
        parent_state,
        expression,
        effect,
        facts,
        relation_notes,
        support_rank,
        stress_rank,
    )
    bottleneck_label = BOTTLENECK_LABELS.get(bottleneck, "")
    if bottleneck_label:
        conditions = tuple(item for item in conditions if item != bottleneck_label)
    evidence = tuple(
        dict.fromkeys(
            item
            for item in (
                natal.evidence_ids
                + luck_item.evidence_ids
                + ((f"annual:{facts.annual.civil_year}",) if facts.annual is not None else ())
            )
            if item
        )
    )
    return TemporalDomainActivationResult(
        domain_id=domain_id,
        natal_state=natal_state,
        luck_activation_state=parent_state,
        annual_modifier=effect,
        annual_expression_state=expression,
        temporal_driver=driver_id,
        temporal_bottleneck=bottleneck,
        support=support,
        stress=stress,
        recovery=recovery,
        conditions=conditions,
        confidence=ConfidenceValue(value=0.68 if expression not in {"unresolved", "blocked"} else 0.4),
        evidence_ids=evidence,
        trace_ids=(f"TR-P7-TA-{domain_id}",),
        envelope=ActivationEnvelope(
            domain_id=domain_id,
            parent_state=parent_state,
            expression_state=expression,
        ),
    )


def dominant_annual_activation(
    items: dict[str, TemporalDomainActivationResult],
    order: tuple[str, ...],
) -> str:
    """Pick the strongest annual expression among published domains."""
    best = ""
    best_rank = -1
    skip = {"dormant", "blocked", "unresolved", "suppressed", "transition"}
    for domain_id in order:
        if domain_id not in MAIN_TEMPORAL_IDS:
            continue
        item = items.get(domain_id)
        if item is None or item.annual_expression_state in skip:
            continue
        rank = EXPRESSION_RANK.get(item.annual_expression_state, 0)
        if rank > best_rank:
            best = domain_id
            best_rank = rank
    return best


def dominant_annual_suppression(
    items: dict[str, TemporalDomainActivationResult],
    order: tuple[str, ...],
) -> str:
    """Pick the first suppressed or high-stress annual expression."""
    for domain_id in order:
        if domain_id not in MAIN_TEMPORAL_IDS:
            continue
        item = items.get(domain_id)
        if item is None:
            continue
        if item.annual_expression_state == "suppressed":
            return domain_id
        if LEVEL_RANK.get(item.stress, 0) >= 3:
            return domain_id
    return ""


def temporal_salience(
    facts: TemporalActivationContext,
    items: dict[str, TemporalDomainActivationResult],
) -> tuple[str, ...]:
    """Rank already-important domains by annual activation. Does not rerank natal EP."""
    ranked = [item for item in facts.evidence_priority.ranked_domains if item in MAIN_TEMPORAL_IDS]
    if not ranked:
        ranked = list(MAIN_TEMPORAL_IDS)
    scored: list[tuple[int, int, str]] = []
    for index, domain_id in enumerate(ranked):
        item = items.get(domain_id)
        if item is None:
            continue
        if item.annual_expression_state in {"dormant", "blocked", "unresolved", "transition"}:
            continue
        scored.append((EXPRESSION_RANK.get(item.annual_expression_state, 0), -index, domain_id))
    scored.sort(reverse=True)
    return tuple(domain_id for _rank, _index, domain_id in scored)


def _order(facts: TemporalActivationContext) -> tuple[str, ...]:
    known = list(facts.luck_cycle_result.order) if facts.luck_cycle_result.order else list(MAIN_ACTIVATION_IDS)
    extra = [item for item in MAIN_ACTIVATION_IDS if item not in known]
    return tuple(item for item in known + extra if item in facts.luck_cycle_result.items or item in facts.natal)


def _parent_state(item: DomainActivationResult | None) -> str:
    if item is None:
        return ""
    return item.activation_state.value


def _ranks(domain_id: str, family: str, facts: TemporalActivationContext) -> tuple[int, int]:
    support_families = DOMAIN_SUPPORT_FAMILIES.get(domain_id, frozenset())
    stress_families = DOMAIN_STRESS_FAMILIES.get(domain_id, frozenset())
    support_rank = 0
    stress_rank = 0
    if family and family in support_families:
        support_rank = 2
        if facts.useful_god_match or facts.element_action in {"support", "generate"}:
            support_rank = 3
    if family and family in stress_families:
        stress_rank = 2
        if family == "peer":
            stress_rank = 3
    if facts.element_action == "drain" and family in support_families:
        support_rank = max(support_rank - 1, 0)
        stress_rank = max(stress_rank, 1)
    if facts.element_action in {"control", "stress"} and family:
        stress_rank = max(stress_rank, 2)
    return support_rank, stress_rank


def _relation_guard(
    domain_id: str,
    family: str,
    support_rank: int,
    stress_rank: int,
    facts: TemporalActivationContext,
    natal: DomainInterpretationResult,
    luck_item: DomainActivationResult,
) -> tuple[int, int, tuple[str, ...]]:
    """Relation presence is not an outcome. Clash is not a bad event."""
    if facts.annual is None or not facts.annual.relations:
        return support_rank, stress_rank, ()
    notes: list[str] = []
    relevant = _domain_relevant(domain_id, family)
    parent = luck_item.activation_state
    for kind in facts.annual.relations:
        if kind == "combination":
            notes.append("Hợp năm này không phải sự kiện tốt")
            if relevant and parent not in {ActivationState.DORMANT, ActivationState.BLOCKED}:
                support_rank = min(support_rank + 1, 3)
        elif kind == "clash":
            notes.append("Xung năm này không phải sự kiện xấu")
            if relevant and natal.state not in {DomainState.BLOCKED}:
                stress_rank = min(stress_rank + 1, 3)
        elif kind in {"punishment", "harm", "break"}:
            notes.append("Hình/hại/phá năm này không phải tai họa")
            if relevant and parent is not ActivationState.DORMANT:
                stress_rank = min(stress_rank + 1, 3)
        elif kind in {"generation", "control"}:
            notes.append("Sinh khắc năm này phải đọc qua natal và Đại Vận")
    return support_rank, stress_rank, tuple(dict.fromkeys(notes))


def _domain_relevant(domain_id: str, family: str) -> bool:
    if family and family in DOMAIN_SUPPORT_FAMILIES.get(domain_id, frozenset()):
        return True
    if family and family in DOMAIN_STRESS_FAMILIES.get(domain_id, frozenset()):
        return True
    return domain_id in {"vitality", "relationship"}


def _modifier_effect(
    domain_id: str,
    family: str,
    support_rank: int,
    stress_rank: int,
    parent_state: str,
    natal_state: str,
) -> str:
    support_families = DOMAIN_SUPPORT_FAMILIES.get(domain_id, frozenset())
    stress_families = DOMAIN_STRESS_FAMILIES.get(domain_id, frozenset())
    support_engaged = bool(family and family in support_families)
    stress_engaged = bool(family and family in stress_families)
    if support_engaged and stress_engaged:
        return "destabilize"
    if not support_engaged and not stress_engaged:
        return "stabilize"
    if stress_engaged and not support_engaged:
        if parent_state == "overloaded":
            return "recover"
        if parent_state in {"strong", "peak", "moderate"}:
            return "suppress"
        return "stress"
    if parent_state == "dormant":
        return "activate"
    if natal_state in NATAL_LIMITED and parent_state in {"conditional", "weak"}:
        return "open_condition" if support_rank >= 2 else "strengthen"
    if parent_state == "overloaded":
        return "strengthen"
    return "strengthen"


def _overloaded(
    domain_id: str,
    natal_state: str,
    parent_state: str,
    support_rank: int,
    effect: str,
) -> bool:
    if effect not in {"strengthen", "activate"}:
        return False
    if domain_id not in OVERLOAD_DOMAINS or support_rank < 3:
        return False
    if parent_state == "overloaded":
        return True
    if parent_state in {"strong", "peak"} and natal_state in NATAL_LIMITED:
        return True
    return natal_state in NATAL_LIMITED and parent_state in {"moderate", "conditional", "strong"}


def _expression(
    parent_state: str,
    effect: str,
    support_rank: int,
    natal_state: str,
    overloaded: bool,
) -> str:
    if natal_state in NATAL_MISSING:
        return "unresolved"
    if parent_state in {"blocked", "unresolved"}:
        return parent_state
    if overloaded:
        return "overloaded"
    if effect == "recover" and parent_state in {"overloaded", "suppressed", "strong", "peak"}:
        return "recovering"
    if effect == "stabilize":
        return "dormant" if parent_state == "dormant" else "transition"
    if effect == "activate" and parent_state == "dormant":
        return "weak" if support_rank < 3 else "active"
    if effect in {"suppress", "weaken"}:
        if parent_state == "overloaded":
            return "recovering"
        if parent_state in {"strong", "peak"}:
            return "weak"
        return "suppressed"
    if effect == "stress":
        if parent_state == "dormant":
            return "weak"
        if parent_state in {"strong", "peak"}:
            return "active"
        return "conditional" if parent_state == "conditional" else parent_state
    if effect == "destabilize":
        return "conditional"
    if effect == "open_condition":
        return "conditional"
    if effect == "block_condition":
        return "suppressed"
    if effect == "strengthen":
        if parent_state == "overloaded":
            return "overloaded"
        if parent_state == "dormant":
            return "weak"
        if parent_state == "peak":
            return "peak"
        if parent_state == "strong" and natal_state in NATAL_STRONG and support_rank >= 3:
            return "peak"
        if parent_state == "strong":
            return "strong"
        if parent_state == "moderate":
            return "active" if support_rank < 3 else "strong"
        if parent_state == "conditional":
            return "conditional"
        return "active"
    return "transition"


def _driver_id(expression: str, effect: str, facts: TemporalActivationContext) -> str:
    if expression in {"dormant", "blocked"} or effect == "stabilize":
        return "not_applicable"
    if expression == "unresolved":
        return "unresolved"
    if facts.annual is None:
        return "not_applicable"
    if "clash" in facts.annual.relations:
        clash_driver = "annual_clash_pressure"
        if clash_driver in TEMPORAL_DRIVER_IDS and effect in {"stress", "suppress"}:
            god_driver = GOD_TO_ANNUAL_DRIVER.get(facts.annual.god_id, "")
            return god_driver or clash_driver
    driver = GOD_TO_ANNUAL_DRIVER.get(facts.annual.god_id, "")
    if driver in TEMPORAL_DRIVER_IDS:
        return driver
    if facts.useful_god_match:
        return "annual_useful_god"
    if facts.element_action in {"support", "generate"}:
        return "annual_element_support"
    if facts.element_action == "drain":
        return "annual_element_drain"
    if facts.element_action in {"control", "stress"}:
        return "annual_element_control"
    return "not_applicable"


def _bottleneck(
    domain_id: str,
    family: str,
    parent_state: str,
    expression: str,
    stress_rank: int,
) -> str:
    if expression == "overloaded" or parent_state == "overloaded":
        if expression == "recovering":
            return "annual_parent_overload"
        return "annual_carrying_capacity"
    if family == "peer" and stress_rank >= 2:
        return "annual_peer_pressure"
    if family == "officer" and domain_id in {"vitality", "relationship"}:
        return "annual_officer_pressure"
    if family == "output" and domain_id == "authority":
        return "annual_output_vs_officer"
    if expression == "conditional":
        return "annual_carrying_capacity"
    return "none"


def _conditions(
    natal_state: str,
    parent_state: str,
    expression: str,
    effect: str,
    facts: TemporalActivationContext,
    relation_notes: tuple[str, ...],
    support_rank: int,
    stress_rank: int,
) -> tuple[str, ...]:
    items: list[str] = list(relation_notes)
    if natal_state in NATAL_LIMITED and expression not in {"dormant", "blocked"}:
        items.append("Sức chứa natal hạn chế biểu đạt năm này")
    if parent_state == "overloaded" and expression == "recovering":
        items.append("Đại vận vẫn quá tải; lưu niên chỉ giảm áp biểu đạt")
    if effect == "strengthen" and expression == "overloaded":
        items.append("Thêm kích hoạt năm này không tự động tốt hơn")
    if effect == "activate" and parent_state == "dormant":
        items.append("Lưu niên không thay Đại Vận đang ngủ")
    if facts.useful_god_match and expression not in {"peak", "dormant"}:
        items.append("Khớp Dụng Thần năm này chưa đủ để đạt đỉnh")
    if facts.damage_types and stress_rank > 0:
        items.append("damage_activation")
    if facts.has_rescue and support_rank > 0:
        items.append("rescue_activation")
    return tuple(dict.fromkeys(items))


def _recovery_level(effect: str, expression: str) -> str:
    if effect == "recover" or expression == "recovering":
        return "moderate"
    return "none"


def _level(rank: int) -> str:
    index = min(max(rank, 0), len(LEVELS) - 1)
    return LEVELS[index]


def _empty(
    domain_id: str,
    parent_state: str,
    natal_state: str,
) -> TemporalDomainActivationResult:
    return TemporalDomainActivationResult(
        domain_id=domain_id,
        natal_state=natal_state,
        luck_activation_state=parent_state,
        annual_modifier="stabilize",
        annual_expression_state="unresolved",
        temporal_driver="unresolved",
        confidence=ConfidenceValue(value=0.3),
        trace_ids=(f"TR-P7-TA-{domain_id}",),
        envelope=ActivationEnvelope(domain_id=domain_id, parent_state=parent_state, expression_state="unresolved"),
    )


def _copy_parent(
    natal: DomainInterpretationResult,
    luck_item: DomainActivationResult,
    modifier: str,
    expression: str,
    support: str,
    stress: str,
    recovery: str,
) -> TemporalDomainActivationResult:
    parent_state = luck_item.activation_state.value
    return TemporalDomainActivationResult(
        domain_id=natal.domain_id,
        natal_state=natal.state.value,
        luck_activation_state=parent_state,
        annual_modifier=modifier,
        annual_expression_state=expression,
        temporal_driver="not_applicable" if expression in {"blocked", "dormant"} else "unresolved",
        support=support,
        stress=stress,
        recovery=recovery,
        confidence=ConfidenceValue(value=0.4),
        evidence_ids=natal.evidence_ids,
        trace_ids=(f"TR-P7-TA-{natal.domain_id}",),
        envelope=ActivationEnvelope(
            domain_id=natal.domain_id,
            parent_state=parent_state,
            expression_state=expression,
        ),
    )


def luck_layer_domains(luck: LuckActivationResult) -> dict[str, TemporalDomainActivationResult]:
    """Bind luck-cycle expression by copy. Does not recompute activation."""
    items: dict[str, TemporalDomainActivationResult] = {}
    for domain_id, item in luck.items.items():
        parent_state = item.activation_state.value
        items[domain_id] = TemporalDomainActivationResult(
            domain_id=domain_id,
            natal_state=item.natal_state,
            luck_activation_state=parent_state,
            annual_modifier="stabilize",
            annual_expression_state=parent_state if parent_state in EXPRESSION_RANK else "unresolved",
            temporal_driver="not_applicable",
            temporal_bottleneck="none",
            support=item.support,
            stress=item.stress,
            recovery="none",
            conditions=(),
            confidence=item.confidence,
            evidence_ids=item.evidence_ids,
            trace_ids=(f"TR-P7-TA-luck-{domain_id}",),
            envelope=ActivationEnvelope(
                domain_id=domain_id,
                parent_layer="natal",
                parent_state=item.natal_state,
                child_layer="luck_cycle",
                expression_state=parent_state,
            ),
        )
    return items


def layer_modifiers(items: dict[str, TemporalDomainActivationResult]) -> tuple[TemporalActivationModifier, ...]:
    """One modifier per domain. No good/bad flag."""
    return tuple(
        TemporalActivationModifier(
            domain_id=domain_id,
            effect=item.annual_modifier,
            conditions=item.conditions,
        )
        for domain_id, item in items.items()
    )
