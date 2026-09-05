"""Evaluate luck-window expression. Does not rewrite natal capability."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domains import DomainInterpretationResult
from engines.detailed_interpretation_engine.enums import ActivationState, DomainState
from engines.detailed_interpretation_engine.luck_activation.constants import (
    ACTIVATION_DRIVER_IDS,
    DOMAIN_STRESS_FAMILIES,
    DOMAIN_SUPPORT_FAMILIES,
    GOD_TO_DRIVER,
    KNOWN_ACTIVATION_IDS,
    LEVEL_RANK,
    MAIN_ACTIVATION_IDS,
    NATAL_LIMITED,
    NATAL_MISSING,
    NATAL_STRONG,
    OVERLOAD_DOMAINS,
    STATE_RANK,
    SUPPORT_ACTIVATION_IDS,
)
from engines.detailed_interpretation_engine.luck_activation.facts import LuckActivationFacts
from engines.detailed_interpretation_engine.luck_activation.labels import (
    BOTTLENECK_LABELS,
    DRIVER_LABELS,
)
from engines.detailed_interpretation_engine.luck_activation.models import DomainActivationResult
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_LEVELS: tuple[str, ...] = ("none", "low", "moderate", "high", "excessive")


def activation_order(facts: LuckActivationFacts) -> tuple[str, ...]:
    """Keep natal domain order. Do not rerank by luck volume."""
    known = list(facts.domains.order) if facts.domains.order else list(MAIN_ACTIVATION_IDS)
    extra = [item for item in MAIN_ACTIVATION_IDS + SUPPORT_ACTIVATION_IDS if item not in known]
    return tuple(item for item in known + extra if item in KNOWN_ACTIVATION_IDS)


def evaluate_domain_activations(
    facts: LuckActivationFacts,
) -> dict[str, DomainActivationResult]:
    """Build one activation object per known domain."""
    return {
        domain_id: evaluate_domain_activation(domain_id, facts)
        for domain_id in activation_order(facts)
    }


def evaluate_domain_activation(
    domain_id: str,
    facts: LuckActivationFacts,
) -> DomainActivationResult:
    """Measure expression opportunity for one natal domain in this luck window."""
    natal = facts.natal.get(domain_id)
    if natal is None:
        return _empty(domain_id, ActivationState.BLOCKED, "not_applicable")
    natal_state = natal.state.value
    if natal.state in {DomainState.NOT_EVALUATED, DomainState.UNRESOLVED}:
        return _from_natal(natal, ActivationState.UNRESOLVED, "unresolved", (), "none", "none", (), ())
    if natal.state is DomainState.BLOCKED:
        return _from_natal(natal, ActivationState.BLOCKED, "not_applicable", (), "none", "none", (), ())
    family = facts.temporal_family
    support_rank, stress_rank = _ranks(domain_id, family, facts)
    overloaded = _overloaded(domain_id, natal_state, family, support_rank, facts)
    state = _state(natal_state, support_rank, stress_rank, family, domain_id, overloaded)
    types = _types(domain_id, family, support_rank, stress_rank, state, facts)
    driver_id = _driver_id(state, facts)
    bottleneck = _bottleneck(domain_id, family, state, stress_rank)
    conditions = _conditions(natal_state, state, facts)
    bottleneck_label = BOTTLENECK_LABELS.get(bottleneck, "")
    if bottleneck_label:
        conditions = tuple(item for item in conditions if item != bottleneck_label)
    warnings = _warnings(state)
    support = _level(support_rank if not overloaded else max(support_rank, 4))
    stress = _level(stress_rank if state is not ActivationState.OVERLOADED else max(stress_rank, 3))
    evidence = natal.evidence_ids or natal.supporting_evidence_ids
    if facts.cycle:
        evidence = evidence + (f"luck:{facts.cycle.cycle_id}",)
    return DomainActivationResult(
        domain_id=domain_id,
        natal_state=natal_state,
        natal_driver_id=natal.driver_id,
        natal_driver=natal.driver,
        natal_bottleneck=natal.bottleneck,
        activation_state=state,
        activation_types=types,
        activation_driver=DRIVER_LABELS.get(driver_id, ""),
        activation_driver_id=driver_id,
        activation_bottleneck=bottleneck_label,
        support=support,
        stress=stress,
        conditions=conditions,
        warnings=warnings,
        confidence=ConfidenceValue(value=0.72 if state is not ActivationState.UNRESOLVED else 0.4),
        evidence_ids=tuple(dict.fromkeys(item for item in evidence if item)),
        trace_ids=(f"TR-P7-LA-{domain_id}",),
    )


def dominant_activation_id(items: dict[str, DomainActivationResult], order: tuple[str, ...]) -> str:
    """Pick the strongest engaged activation among published domains."""
    best = ""
    best_rank = -1
    for domain_id in order:
        if domain_id not in MAIN_ACTIVATION_IDS:
            continue
        item = items.get(domain_id)
        if item is None:
            continue
        if item.activation_state in {
            ActivationState.DORMANT,
            ActivationState.BLOCKED,
            ActivationState.UNRESOLVED,
            ActivationState.SUPPRESSED,
        }:
            continue
        rank = STATE_RANK.get(item.activation_state, 0)
        if rank > best_rank:
            best = domain_id
            best_rank = rank
    return best


def dominant_suppression_id(items: dict[str, DomainActivationResult], order: tuple[str, ...]) -> str:
    """Pick the first suppressed or high-stress published domain."""
    for domain_id in order:
        if domain_id not in MAIN_ACTIVATION_IDS:
            continue
        item = items.get(domain_id)
        if item is None:
            continue
        if item.activation_state is ActivationState.SUPPRESSED:
            return domain_id
        if LEVEL_RANK.get(item.stress, 0) >= 3:
            return domain_id
    return ""


def _ranks(domain_id: str, family: str, facts: LuckActivationFacts) -> tuple[int, int]:
    support_families = DOMAIN_SUPPORT_FAMILIES.get(domain_id, frozenset())
    stress_families = DOMAIN_STRESS_FAMILIES.get(domain_id, frozenset())
    support_rank = 0
    stress_rank = 0
    if family and family in support_families:
        support_rank = 2
        if facts.useful_god_match:
            support_rank = 3
    if family and family in stress_families:
        stress_rank = 2
        if family == "peer":
            stress_rank = 3
    return support_rank, stress_rank


def _overloaded(
    domain_id: str,
    natal_state: str,
    family: str,
    support_rank: int,
    facts: LuckActivationFacts,
) -> bool:
    if domain_id not in OVERLOAD_DOMAINS or support_rank < 3:
        return False
    if natal_state in NATAL_LIMITED:
        return True
    if "resource_overload" in facts.damage_types and family in {"officer", "resource"}:
        return domain_id in {"authority", "vitality"}
    return False


def _state(
    natal_state: str,
    support_rank: int,
    stress_rank: int,
    family: str,
    domain_id: str,
    overloaded: bool,
) -> ActivationState:
    if natal_state in NATAL_MISSING:
        return ActivationState.UNRESOLVED
    if overloaded:
        return ActivationState.OVERLOADED
    support_families = DOMAIN_SUPPORT_FAMILIES.get(domain_id, frozenset())
    stress_families = DOMAIN_STRESS_FAMILIES.get(domain_id, frozenset())
    support_engaged = bool(family and family in support_families)
    stress_engaged = bool(family and family in stress_families)
    if not support_engaged and not stress_engaged:
        return ActivationState.DORMANT
    if stress_engaged and not support_engaged:
        return ActivationState.SUPPRESSED
    if natal_state in NATAL_LIMITED:
        return ActivationState.CONDITIONAL
    if support_rank >= 3 and natal_state == DomainState.VERY_STRONG.value and stress_rank == 0:
        return ActivationState.PEAK
    if support_rank >= 3 and natal_state in NATAL_STRONG and stress_rank <= 1:
        return ActivationState.STRONG
    if support_rank >= 2:
        return ActivationState.MODERATE
    if support_rank >= 1 or stress_rank >= 1:
        return ActivationState.WEAK
    return ActivationState.DORMANT


def _types(
    domain_id: str,
    family: str,
    support_rank: int,
    stress_rank: int,
    state: ActivationState,
    facts: LuckActivationFacts,
) -> tuple[str, ...]:
    items: list[str] = []
    if state is ActivationState.SUPPRESSED:
        items.append("suppression")
        items.append("restriction")
    elif state is ActivationState.DORMANT:
        return ()
    elif support_rank > 0:
        items.append("activation")
        items.append("support")
        if facts.useful_god_match:
            items.append("opportunity")
    if stress_rank > 0:
        items.append("stress")
    if family == "resource" and domain_id in {"vitality", "authority"}:
        items.append("recovery")
    if facts.damage_types and stress_rank > 0:
        items.append("damage_activation")
    if facts.has_rescue and support_rank > 0:
        items.append("rescue_activation")
    if state is ActivationState.OVERLOADED:
        items.append("restriction")
    unique: list[str] = []
    for item in items:
        if item not in unique:
            unique.append(item)
    return tuple(unique)


def _driver_id(state: ActivationState, facts: LuckActivationFacts) -> str:
    if state in {ActivationState.DORMANT, ActivationState.BLOCKED}:
        return "not_applicable"
    if state is ActivationState.UNRESOLVED:
        return "unresolved"
    driver = GOD_TO_DRIVER.get(facts.temporal_god_id, "")
    if driver in ACTIVATION_DRIVER_IDS:
        return driver
    if facts.useful_god_match:
        return "temporal_useful_god"
    if facts.support_elements:
        return "temporal_element_support"
    if facts.attack_elements:
        return "temporal_element_drain"
    return "not_applicable"


def _bottleneck(domain_id: str, family: str, state: ActivationState, stress_rank: int) -> str:
    if state is ActivationState.OVERLOADED:
        return "carrying_capacity"
    if family == "peer" and stress_rank >= 2:
        return "peer_luck_pressure"
    if family == "officer" and domain_id in {"vitality", "relationship"}:
        return "officer_luck_pressure"
    if family == "output" and domain_id == "authority":
        return "output_vs_officer"
    if family == "resource" and state is ActivationState.OVERLOADED:
        return "resource_overload_window"
    if state is ActivationState.CONDITIONAL:
        return "carrying_capacity"
    return "none"


def _conditions(natal_state: str, state: ActivationState, facts: LuckActivationFacts) -> tuple[str, ...]:
    if state in {ActivationState.DORMANT, ActivationState.BLOCKED, ActivationState.UNRESOLVED}:
        return ()
    items: list[str] = []
    if natal_state in NATAL_LIMITED:
        items.append("Sức chứa natal hạn chế biểu đạt")
    if facts.useful_god_match and state is not ActivationState.PEAK:
        items.append("Khớp Dụng Thần chưa đủ để đạt đỉnh")
    if state is ActivationState.OVERLOADED:
        items.append("Lực vận vượt sức chứa natal")
    if state is ActivationState.CONDITIONAL:
        items.append("Biểu đạt phụ thuộc điều kiện natal")
    return tuple(items)


def _warnings(state: ActivationState) -> tuple[str, ...]:
    if state in {ActivationState.STRONG, ActivationState.PEAK, ActivationState.OVERLOADED}:
        return ("not_an_event_prediction",)
    return ()


def _level(rank: int) -> str:
    index = min(max(rank, 0), len(_LEVELS) - 1)
    return _LEVELS[index]


def _empty(
    domain_id: str,
    state: ActivationState,
    driver_id: str,
) -> DomainActivationResult:
    return DomainActivationResult(
        domain_id=domain_id,
        natal_state="",
        natal_driver_id="",
        activation_state=state,
        activation_driver=DRIVER_LABELS.get(driver_id, ""),
        activation_driver_id=driver_id,
        confidence=ConfidenceValue(value=0.3),
        trace_ids=(f"TR-P7-LA-{domain_id}",),
    )


def _from_natal(
    natal: DomainInterpretationResult,
    state: ActivationState,
    driver_id: str,
    types: tuple[str, ...],
    support: str,
    stress: str,
    conditions: tuple[str, ...],
    warnings: tuple[str, ...],
) -> DomainActivationResult:
    return DomainActivationResult(
        domain_id=natal.domain_id,
        natal_state=natal.state.value,
        natal_driver_id=natal.driver_id,
        natal_driver=natal.driver,
        natal_bottleneck=natal.bottleneck,
        activation_state=state,
        activation_types=types,
        activation_driver=DRIVER_LABELS.get(driver_id, ""),
        activation_driver_id=driver_id,
        support=support,
        stress=stress,
        conditions=conditions,
        warnings=warnings,
        confidence=ConfidenceValue(value=0.4),
        evidence_ids=natal.evidence_ids,
        trace_ids=(f"TR-P7-LA-{natal.domain_id}",),
    )
