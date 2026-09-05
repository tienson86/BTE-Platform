"""Evaluate activation-to-activation findings. Does not rewrite activation or natal domain."""

from __future__ import annotations

from engines.detailed_interpretation_engine.domains import DomainGraphEdge
from engines.detailed_interpretation_engine.enums import ActivationState, EvaluationStatus
from engines.detailed_interpretation_engine.luck_activation.models import DomainActivationResult
from engines.detailed_interpretation_engine.luck_interaction.constants import (
    DRIVER_SENTINELS,
    ENGAGED_STATES,
    LOUD_STATES,
    QUIET_STATES,
    STRESSED_STATES,
    STRENGTH_RANK,
    TYPE_TO_RELATION,
)
from engines.detailed_interpretation_engine.luck_interaction.facts import LuckInteractionFacts
from engines.detailed_interpretation_engine.luck_interaction.labels import DOMAIN_TITLES
from engines.detailed_interpretation_engine.luck_interaction.models import (
    DomainInteractionFinding,
    InteractionPriority,
    LifeSituationResult,
    ResourceShift,
    StressTransfer,
)
from engines.detailed_interpretation_engine.temporal import LuckActivationResult
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_SUPPORT_RELATIONS = frozenset({"supports", "reinforces"})
_CONFLICT_RELATIONS = frozenset({"conflicts"})


def evaluate_findings(facts: LuckInteractionFacts) -> tuple[DomainInteractionFinding, ...]:
    """Derive interaction findings from natal DomainGraph plus current activations."""
    activation = facts.activation
    if activation.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return ()
    items = activation.items
    findings: list[DomainInteractionFinding] = []
    seen: set[tuple[str, str, str]] = set()
    for edge in facts.domains.graph.edges:
        if not edge.evidence_ids or edge.source == edge.target:
            continue
        source = items.get(edge.source)
        target = items.get(edge.target)
        if source is None or target is None:
            continue
        skipped = {ActivationState.BLOCKED, ActivationState.UNRESOLVED}
        if source.activation_state in skipped or target.activation_state in skipped:
            continue
        for finding in _from_natal_edge(edge, source, target):
            key = (finding.source_domain, finding.target_domain, finding.interaction_type)
            if key in seen:
                continue
            seen.add(key)
            findings.append(finding)
    return tuple(findings)


def build_priority(findings: tuple[DomainInteractionFinding, ...]) -> InteractionPriority:
    """Pick highest window interactions. Does not rerank natal Evidence Priority."""
    return InteractionPriority(
        highest_interaction=_highest(findings, None),
        highest_conflict=_highest(findings, {"conflict"}),
        highest_opportunity=_highest(findings, {"support", "reinforcement"}),
        highest_trade_off=_highest(findings, {"trade_off", "blocked_expression"}),
        highest_stress=_highest(findings, {"stress_transfer", "resource_shift"}),
        highest_recovery=_highest(findings, {"recovery"}),
    )


def elect_interaction_driver(findings: tuple[DomainInteractionFinding, ...]) -> str:
    """Activated domain with the strongest downstream effect this window."""
    scores: dict[str, int] = {}
    for finding in findings:
        if finding.interaction_type == "unresolved":
            continue
        scores[finding.source_domain] = scores.get(finding.source_domain, 0) + STRENGTH_RANK.get(
            finding.strength, 0
        )
    if not scores:
        return "not_applicable"
    return max(scores, key=lambda domain_id: (scores[domain_id], -_order_index(domain_id)))


def elect_interaction_bottleneck(findings: tuple[DomainInteractionFinding, ...]) -> str:
    """Activated domain or condition limiting other activated domains."""
    limiting = {
        "stress_transfer",
        "resource_shift",
        "blocked_expression",
        "trade_off",
        "conflict",
    }
    scores: dict[str, int] = {}
    for finding in findings:
        if finding.interaction_type not in limiting:
            continue
        target = finding.target_domain
        scores[target] = scores.get(target, 0) + STRENGTH_RANK.get(finding.strength, 0)
    if not scores:
        return "not_applicable"
    return max(scores, key=lambda domain_id: (scores[domain_id], -_order_index(domain_id)))


def build_life_situation(
    activation: LuckActivationResult,
    findings: tuple[DomainInteractionFinding, ...],
    driver: str,
    bottleneck: str,
) -> LifeSituationResult:
    """Summarize the luck-window interaction. Insufficient evidence stays unresolved."""
    if not findings:
        return LifeSituationResult(
            situation_id="unresolved",
            situation_state="unresolved",
            temporality="window_bound",
        )
    types = {item.interaction_type for item in findings}
    sources = {item.source_domain for item in findings}
    cost = tuple(
        dict.fromkeys(
            item.target_domain
            for item in findings
            if item.interaction_type in {"trade_off", "stress_transfer", "resource_shift", "blocked_expression"}
        )
    )
    situation = "balanced_growth"
    if "resource_shift" in types or "stress_transfer" in types:
        situation = "resource_pressure"
    elif "blocked_expression" in types and not {"support", "reinforcement"} & types:
        situation = "blocked_growth"
    elif "career" in sources and any(
        item.interaction_type == "support" and item.target_domain == "career" for item in findings
    ):
        situation = "career_expansion"
        career = activation.items.get("career")
        if career is not None and career.activation_state is ActivationState.OVERLOADED:
            situation = "resource_pressure"
    elif "authority" in sources and driver == "authority":
        situation = "authority_consolidation"
    elif any(item.source_domain == "relationship" or item.target_domain == "relationship" for item in findings) and (
        {"conflict", "trade_off"} & types
    ):
        situation = "relationship_stress"
    elif "creative" in sources and any(item.interaction_type == "reinforcement" for item in findings):
        situation = "creative_expansion"
    elif "academic" in sources or "learning" in sources:
        situation = "learning_phase"
    elif "recovery" in {
        kind
        for item in activation.items.values()
        for kind in item.activation_types
    } and not ({"stress_transfer", "resource_shift"} & types):
        situation = "recovery_phase"
    primary = tuple(
        dict.fromkeys(
            [driver] + [item.source_domain for item in findings if item.interaction_type in {"support", "reinforcement"}]
        )
    )
    if driver in DRIVER_SENTINELS:
        primary = tuple(dict.fromkeys(item.source_domain for item in findings))
    ids = tuple(item.finding_id for item in findings)
    return LifeSituationResult(
        situation_id=situation,
        situation_state=situation,
        primary_domain_ids=primary,
        cost_domain_ids=cost,
        summary_keys=(situation,),
        supporting_finding_ids=ids,
        confidence=ConfidenceValue(value=0.7, summary="luck_interaction"),
        temporality="window_bound",
        trace_ids=("TR-P7-LI-situation",),
    )


def highest_opportunity_text(findings: tuple[DomainInteractionFinding, ...]) -> str:
    """Customer-safe opportunity line from the strongest support/reinforcement."""
    finding = _finding(_highest(findings, {"support", "reinforcement"}), findings)
    if finding is None:
        return ""
    source = DOMAIN_TITLES.get(finding.source_domain, finding.source_domain)
    target = DOMAIN_TITLES.get(finding.target_domain, finding.target_domain)
    if finding.interaction_type == "reinforcement":
        return f"{source} gia cố {target}"
    return f"{source} hỗ trợ {target}"


def highest_risk_text(findings: tuple[DomainInteractionFinding, ...]) -> str:
    """Customer-safe risk/trade-off line. Not an event prediction."""
    finding = _finding(
        _highest(findings, {"stress_transfer", "resource_shift", "trade_off", "blocked_expression", "conflict"}),
        findings,
    )
    if finding is None:
        return ""
    source = DOMAIN_TITLES.get(finding.source_domain, finding.source_domain)
    target = DOMAIN_TITLES.get(finding.target_domain, finding.target_domain)
    if finding.interaction_type == "stress_transfer":
        return f"{source} chuyển áp lực sang {target}"
    if finding.interaction_type == "resource_shift":
        return f"{source} dồn sức chứa của {target}"
    if finding.interaction_type == "blocked_expression":
        return f"{source} chưa chuyển thành biểu đạt {target}"
    if finding.interaction_type == "trade_off":
        return f"Tăng {source} đi cùng áp lực {target}"
    return f"{source} xung đột với {target}"


def _from_natal_edge(
    edge: DomainGraphEdge,
    source: DomainActivationResult,
    target: DomainActivationResult,
) -> tuple[DomainInteractionFinding, ...]:
    items: list[DomainInteractionFinding] = []
    if edge.relation in _SUPPORT_RELATIONS:
        if _engaged(source) and _engaged(target):
            kind = "reinforcement" if edge.relation == "reinforces" else "support"
            items.append(
                _finding_of(
                    source,
                    target,
                    kind,
                    edge,
                    opportunities=(_pair_copy(source.domain_id, target.domain_id, kind),),
                )
            )
        elif _loud(source) and _quiet(target):
            items.append(
                _finding_of(
                    source,
                    target,
                    "blocked_expression",
                    edge,
                    conditions=("Biểu đạt đích còn bị kìm bởi sức chứa hoặc kích hoạt yếu",),
                    risks=("Biểu đạt nguồn chưa chuyển thành biểu đạt đích",),
                )
            )
        if _stressed(target) and _capacity_edge(edge):
            items.extend(_capacity_pressure(target, source, edge))
    if edge.relation in _CONFLICT_RELATIONS and (_engaged(source) or _engaged(target)):
        items.append(
            _finding_of(
                source,
                target,
                "conflict",
                edge,
                risks=("Hai kích hoạt cùng hiện hữu, không bị gộp",),
            )
        )
        if _loud(source) and _quiet(target):
            items.append(
                _finding_of(
                    source,
                    target,
                    "trade_off",
                    edge,
                    conditions=("Đánh đổi biểu đạt, không xóa năng lực gốc",),
                    risks=(_pair_copy(source.domain_id, target.domain_id, "trade_off"),),
                )
            )
    return tuple(items)


def _capacity_pressure(
    consumer: DomainActivationResult,
    capacity: DomainActivationResult,
    edge: DomainGraphEdge,
) -> tuple[DomainInteractionFinding, ...]:
    intensity = "high" if consumer.activation_state is ActivationState.OVERLOADED else "moderate"
    evidence = edge.evidence_ids + consumer.evidence_ids
    trace = (f"TR-P7-LI-{consumer.domain_id}-{capacity.domain_id}",)
    shift = ResourceShift(
        from_domain=consumer.domain_id,
        to_domain=capacity.domain_id,
        capacity_kind="structural_capacity",
        intensity=intensity,
        evidence_ids=evidence,
        trace_ids=trace,
    )
    transfer = StressTransfer(
        source_domain=consumer.domain_id,
        target_domain=capacity.domain_id,
        source_stress_level=consumer.stress or consumer.activation_state.value,
        transferred_kind="expression_pressure",
        intensity=intensity,
        evidence_ids=evidence,
        trace_ids=trace,
    )
    return (
        _finding_of(
            consumer,
            capacity,
            "resource_shift",
            edge,
            strength=intensity if intensity in STRENGTH_RANK else "high",
            resource_shift=shift,
            conditions=("Sức chứa hạn chế biểu đạt đồng thời",),
            risks=("Dồn nguồn lực, không đổi năng lực gốc",),
        ),
        _finding_of(
            consumer,
            capacity,
            "stress_transfer",
            edge,
            strength=intensity if intensity in STRENGTH_RANK else "high",
            stress_transfer=transfer,
            conditions=("Áp lực nghề nghiệp cần kiểm soát sức bền biểu đạt",),
            risks=("Chuyển áp lực biểu đạt, không kết luận sức khỏe",),
        ),
    )


def _finding_of(
    source: DomainActivationResult,
    target: DomainActivationResult,
    interaction_type: str,
    edge: DomainGraphEdge,
    *,
    strength: str = "",
    conditions: tuple[str, ...] = (),
    risks: tuple[str, ...] = (),
    opportunities: tuple[str, ...] = (),
    resource_shift: ResourceShift | None = None,
    stress_transfer: StressTransfer | None = None,
) -> DomainInteractionFinding:
    evidence = tuple(dict.fromkeys(edge.evidence_ids + source.evidence_ids + target.evidence_ids))
    chosen = strength or _strength(source, target, interaction_type)
    return DomainInteractionFinding(
        finding_id=f"DI-10-{source.domain_id}-{target.domain_id}-{interaction_type}",
        source_domain=source.domain_id,
        target_domain=target.domain_id,
        interaction_type=interaction_type,
        strength=chosen,
        conditions=conditions,
        risks=risks,
        opportunities=opportunities,
        evidence_ids=evidence,
        trace_ids=(f"TR-P7-LI-{source.domain_id}-{target.domain_id}",),
        natal_edge_ref=f"{edge.source}:{edge.relation}:{edge.target}",
        resource_shift=resource_shift,
        stress_transfer=stress_transfer,
        confidence=ConfidenceValue(value=0.7),
    )


def _capacity_edge(edge: DomainGraphEdge) -> bool:
    return edge.relation == "supports" and edge.source in {"vitality", "relationship", "legacy"}


def _engaged(item: DomainActivationResult) -> bool:
    return item.activation_state in ENGAGED_STATES


def _loud(item: DomainActivationResult) -> bool:
    if item.activation_state in LOUD_STATES:
        return True
    return item.support in {"high", "excessive"}


def _quiet(item: DomainActivationResult) -> bool:
    return item.activation_state in QUIET_STATES


def _stressed(item: DomainActivationResult) -> bool:
    return item.activation_state in STRESSED_STATES or item.stress in {"high", "excessive"}


def _strength(source: DomainActivationResult, target: DomainActivationResult, kind: str) -> str:
    if source.activation_state is ActivationState.OVERLOADED or target.activation_state is ActivationState.OVERLOADED:
        return "high"
    if kind in {"support", "reinforcement"} and source.activation_state in {
        ActivationState.STRONG,
        ActivationState.PEAK,
    }:
        return "high"
    return "moderate"


def _pair_copy(source: str, target: str, kind: str) -> str:
    left = DOMAIN_TITLES.get(source, source)
    right = DOMAIN_TITLES.get(target, target)
    if kind == "trade_off":
        return f"Tăng {left} đi cùng hạn chế biểu đạt {right}"
    if kind == "reinforcement":
        return f"{left} gia cố {right}"
    return f"{left} hỗ trợ {right}"


def _highest(
    findings: tuple[DomainInteractionFinding, ...],
    types: set[str] | None,
) -> str:
    ranked = [
        item
        for item in findings
        if types is None or item.interaction_type in types
    ]
    if not ranked:
        return ""
    ranked.sort(
        key=lambda item: (STRENGTH_RANK.get(item.strength, 0), item.interaction_type, item.finding_id),
        reverse=True,
    )
    return ranked[0].finding_id


def _finding(finding_id: str, findings: tuple[DomainInteractionFinding, ...]) -> DomainInteractionFinding | None:
    if not finding_id:
        return None
    for item in findings:
        if item.finding_id == finding_id:
            return item
    return None


def _order_index(domain_id: str) -> int:
    order = {
        "authority": 0,
        "career": 1,
        "wealth": 2,
        "relationship": 3,
        "legacy": 4,
        "vitality": 5,
    }
    return order.get(domain_id, 9)


def relation_of(interaction_type: str) -> str:
    """Map a finding type onto the frozen interaction graph relation."""
    return TYPE_TO_RELATION.get(interaction_type, "")
