"""Compose Pack 07 findings into one NarrativeGraph. Does not infer or rerank."""

from __future__ import annotations

import re
from dataclasses import replace

from engines.detailed_interpretation_engine.constants import SCHEMA_COMPOSER
from engines.detailed_interpretation_engine.enums import (
    EvaluationStatus,
    NarrativeEdgeType,
    NarrativeLayer,
    NarrativeNodeType,
    PriorityTier,
)
from engines.detailed_interpretation_engine.evidence import EvidencePriorityFinding
from engines.detailed_interpretation_engine.evidence_priority.constants import (
    SHEN_SHA_SOURCE_KINDS,
    TIER_INDEX,
)
from engines.detailed_interpretation_engine.life_optimization.models import OptimizationAction
from engines.detailed_interpretation_engine.narrative import (
    NarrativeBlock,
    NarrativeEdge,
    NarrativeGraph,
    NarrativeNode,
    NarrativeResult,
)
from engines.detailed_interpretation_engine.narrative_composer.constants import (
    HIGH_CONFIDENCE,
    MAX_EXECUTIVE_SENTENCES,
    MAX_LIST_ITEMS,
    MIN_EXECUTIVE_SENTENCES,
    P0_P1,
)
from engines.detailed_interpretation_engine.narrative_composer.facts import (
    NarrativeComposerFacts,
    narrative_ready,
)
from engines.detailed_interpretation_engine.narrative_composer.labels import (
    ALREADY_NOTED,
    ANNUAL_WINDOW,
    CLOSING_LEAD,
    INTEGRITY_TEMPLATE,
    INTERACTION_TEMPLATE,
    LUCK_WINDOW,
    MATTERS_TEMPLATE,
    NO_EVENT,
    OVERLOAD_TEMPLATE,
    PRIORITY_TEMPLATE,
    QUALIFIED,
    SECTION_TITLES,
    UNCERTAIN,
    WHO_TEMPLATE,
    WHO_UNRESOLVED,
    action_label,
    domain_title,
    integrity_label,
    interaction_label,
    leakage_label,
    luck_state_label,
    reason_label,
    situation_label,
    state_label,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue

_STRENGTH_KINDS = frozenset({"achievement", "career", "ten_gods_ecosystem"})
_IDENTITY_KINDS = frozenset({"grade", "pattern", "purity", "integrity"})
_RISK_KINDS = frozenset({"damage", "wealth", "warning", "condition"})
_OPP_KINDS = frozenset({"achievement", "career", "wealth", "ten_gods_ecosystem"})
_OPP_DOMAINS = frozenset({"career", "wealth", "legacy", "authority", "academic", "creative"})
_CODE_LABEL = re.compile(r"[a-z]{3,}[_:][a-z0-9_]+")


def evaluate_narrative(facts: NarrativeComposerFacts) -> NarrativeResult:
    """Turn ranked Pack 07 findings into story-ordered blocks and a graph."""
    if not narrative_ready(facts):
        return NarrativeResult()
    used: set[str] = set()
    strengths = _list_blocks(facts, "strength", _strength_findings(facts), used)
    risks = _list_blocks(facts, "risk", _risk_findings(facts), used)
    opportunities = _list_blocks(facts, "opportunity", _opportunity_findings(facts), used)
    executive = _executive(facts)
    explained = {item.summary for item in strengths + risks + opportunities if item.summary}
    domains = _domain_blocks(facts, used, explained)
    luck_blocks = _luck_blocks(facts, used)
    actions = _action_blocks(facts)
    closing = _closing(actions)
    raw_blocks = (executive,) + strengths + risks + opportunities + domains + luck_blocks + actions + (closing,)
    blocks = _with_sources(raw_blocks, facts)
    graph = _graph(blocks, facts)
    luck_text = " ".join(item.summary for item in luck_blocks if item.summary)
    action_text = " ".join(item.summary for item in actions if item.summary)
    confidence = _confidence(blocks)
    trace = tuple(
        dict.fromkeys(("TR-P7-NAR",) + tuple(eid for item in blocks for eid in item.evidence_ids))
    )
    return NarrativeResult(
        schema_version=SCHEMA_COMPOSER,
        status=EvaluationStatus.RESOLVED,
        executive_summary=executive.summary,
        strengths=tuple(item.summary for item in strengths),
        risks=tuple(item.summary for item in risks),
        opportunities=tuple(item.summary for item in opportunities),
        domains={item.domain: item.summary for item in domains if item.domain},
        temporal=luck_text,
        luck=luck_text,
        optimization=action_text,
        closing_summary=closing.summary,
        confidence=confidence,
        trace=trace,
        graph=graph,
        blocks=blocks,
        mc01_summary_ref=facts.snapshot.mingju_result_id if facts.snapshot else "",
        layers={
            "commercial": tuple(item.block_id for item in blocks),
            "executive": tuple(item.block_id for item in (executive,) + strengths[:2] + risks[:2] + actions[:3]),
        },
    )


def _strength_findings(facts: NarrativeComposerFacts) -> tuple[EvidencePriorityFinding, ...]:
    items = [
        item
        for item in facts.evidence_priority.findings
        if item.source_kind not in SHEN_SHA_SOURCE_KINDS
        and item.tier is not PriorityTier.P5
        and (
            item.finding_id in facts.evidence_priority.driver_ids
            or item.finding_id in facts.evidence_priority.dominant_evidence
            or item.category in {"opportunity", "driver", "support"}
            or item.source_kind in _STRENGTH_KINDS
        )
        and item.category not in {"risk", "bottleneck", "damage"}
    ]
    return _ranked(items)[:MAX_LIST_ITEMS]


def _risk_findings(facts: NarrativeComposerFacts) -> tuple[EvidencePriorityFinding, ...]:
    items = [
        item
        for item in facts.evidence_priority.findings
        if item.source_kind not in SHEN_SHA_SOURCE_KINDS
        and (
            item.finding_id in facts.evidence_priority.risk_evidence
            or item.finding_id in facts.evidence_priority.bottleneck_ids
            or item.category in {"risk", "bottleneck", "damage"}
            or item.source_kind in _RISK_KINDS
        )
    ]
    return _ranked(items)[:MAX_LIST_ITEMS]


def _opportunity_findings(facts: NarrativeComposerFacts) -> tuple[EvidencePriorityFinding, ...]:
    items = [
        item
        for item in facts.evidence_priority.findings
        if item.source_kind not in SHEN_SHA_SOURCE_KINDS
        and item.tier is not PriorityTier.P5
        and (
            item.finding_id in facts.evidence_priority.opportunity_evidence
            or item.category == "opportunity"
            or (item.source_kind in _OPP_KINDS and item.domain in _OPP_DOMAINS)
        )
        and item.category not in {"risk", "damage"}
    ]
    return _ranked(items)[:MAX_LIST_ITEMS]


def _list_blocks(
    facts: NarrativeComposerFacts,
    kind: str,
    findings: tuple[EvidencePriorityFinding, ...],
    used: set[str],
) -> tuple[NarrativeBlock, ...]:
    blocks: list[NarrativeBlock] = []
    for index, finding in enumerate(findings, start=1):
        if finding.finding_id in used:
            continue
        label = _finding_label(finding)
        if not label:
            continue
        used.add(finding.finding_id)
        summary = label if _high(finding) else f"{label} {QUALIFIED}".strip()
        blocks.append(
            _block(
                f"nar.{kind}.{index}",
                kind,
                finding.tier.value,
                SECTION_TITLES[kind],
                summary,
                evidence_ids=(finding.finding_id,),
                trace_ids=finding.trace_ids + (f"TR-P7-NAR-{kind}",),
                confidence=finding.confidence,
                domain=finding.domain,
            )
        )
    if kind == "risk":
        blocks.extend(_leakage_blocks(facts, used, len(blocks)))
    return tuple(blocks[:MAX_LIST_ITEMS])


def _leakage_blocks(
    facts: NarrativeComposerFacts,
    used: set[str],
    start: int,
) -> tuple[NarrativeBlock, ...]:
    items: list[NarrativeBlock] = []
    for domain_id in facts.domain_order:
        natal = facts.natal.get(domain_id)
        if natal is None or not natal.leakage:
            continue
        key = f"leakage:{domain_id}:{natal.leakage}"
        if key in used:
            continue
        used.add(key)
        leak = leakage_label(natal.leakage) or natal.leakage
        if not leak or leak.startswith("E-DI-") or "TR-P7" in leak:
            continue
        title = domain_title(domain_id)
        summary = f"{title}: rò rỉ {leak}."
        items.append(
            _block(
                f"nar.risk.leak.{domain_id}",
                "risk",
                natal.priority or "P2",
                SECTION_TITLES["risk"],
                summary,
                evidence_ids=natal.evidence_ids[:1],
                trace_ids=natal.trace_ids + ("TR-P7-NAR-risk",),
                confidence=natal.confidence,
                domain=domain_id,
            )
        )
    for domain_id in ("career", "authority"):
        luck = facts.luck.items.get(domain_id)
        if luck is None or luck.activation_state.value != "overloaded":
            continue
        key = f"overload:{domain_id}"
        if key in used:
            continue
        used.add(key)
        summary = OVERLOAD_TEMPLATE.format(
            domain=domain_title(domain_id),
            state=luck_state_label(luck.activation_state.value),
        )
        items.append(
            _block(
                f"nar.risk.overload.{domain_id}",
                "risk",
                "P1",
                SECTION_TITLES["risk"],
                summary,
                evidence_ids=luck.evidence_ids[:1],
                trace_ids=luck.trace_ids + ("TR-P7-NAR-risk",),
                domain=domain_id,
            )
        )
    return tuple(items)


def _executive(facts: NarrativeComposerFacts) -> NarrativeBlock:
    sentences: list[str] = []
    snapshot = facts.snapshot
    if snapshot is None or not snapshot.pattern:
        sentences.append(WHO_UNRESOLVED)
    else:
        sentences.append(
            WHO_TEMPLATE.format(pattern=snapshot.pattern, grade=snapshot.grade or "chưa xếp hạng")
        )
        if snapshot.integrity:
            sentences.append(INTEGRITY_TEMPLATE.format(integrity=integrity_label(snapshot.integrity)))
    for finding in _p0_p1(facts):
        if finding.source_kind in SHEN_SHA_SOURCE_KINDS or finding.source_kind in _IDENTITY_KINDS:
            continue
        label = _finding_label(finding)
        if not label:
            continue
        line = MATTERS_TEMPLATE.format(label=label)
        if line not in sentences:
            sentences.append(line)
        if len(sentences) >= 8:
            break
    action = _top_action(facts)
    if action is not None:
        title = action_label(action.recommended_action_key) or action.recommended_action_key
        if title:
            sentences.append(PRIORITY_TEMPLATE.format(action=title))
    if len(sentences) < MIN_EXECUTIVE_SENTENCES:
        sentences.append(QUALIFIED if snapshot and snapshot.pattern else UNCERTAIN)
    summary = " ".join(sentences[:MAX_EXECUTIVE_SENTENCES])
    evidence = tuple(item.finding_id for item in _p0_p1(facts)[:6])
    return _block(
        "nar.executive",
        "executive_summary",
        "P0",
        SECTION_TITLES["executive_summary"],
        summary,
        evidence_ids=evidence,
        trace_ids=("TR-P7-NAR-executive",),
    )


def _domain_blocks(
    facts: NarrativeComposerFacts,
    used: set[str],
    explained: set[str],
) -> tuple[NarrativeBlock, ...]:
    items: list[NarrativeBlock] = []
    for domain_id in facts.domain_order:
        natal = facts.natal.get(domain_id)
        if natal is None:
            continue
        if natal.state.value in {"not_evaluated", "unresolved", "blocked"}:
            details = (
                state_label(natal.state.value) or UNCERTAIN,
                "",
                "",
                "",
                "",
                "",
            )
            summary = f"{domain_title(domain_id)}: {UNCERTAIN}"
            items.append(
                _block(
                    f"nar.domain.{domain_id}",
                    "domain_section",
                    natal.priority or "P2",
                    domain_title(domain_id),
                    summary,
                    details=details,
                    evidence_ids=natal.evidence_ids[:4],
                    trace_ids=natal.trace_ids + (f"TR-P7-NAR-{domain_id}",),
                    confidence=natal.confidence,
                    domain=domain_id,
                )
            )
            continue
        bottleneck = natal.bottleneck
        if bottleneck and any(bottleneck in item for item in explained):
            bottleneck = ALREADY_NOTED
        leak = leakage_label(natal.leakage) if natal.leakage else ""
        caution = natal.risk or leak
        if caution and any(caution in item for item in explained):
            caution = ALREADY_NOTED
        opportunity = natal.opportunities[0] if natal.opportunities else ""
        condition = natal.condition or (natal.conditions[0] if natal.conditions else "")
        details = (
            state_label(natal.state.value),
            natal.driver,
            bottleneck,
            opportunity,
            caution,
            condition,
        )
        summary = f"{domain_title(domain_id)}: {'; '.join(item for item in details if item)}."
        used.update(natal.evidence_ids[:2])
        explained.add(summary)
        items.append(
            _block(
                f"nar.domain.{domain_id}",
                "domain_section",
                natal.priority or "P2",
                domain_title(domain_id),
                summary,
                details=details,
                evidence_ids=natal.evidence_ids[:4],
                trace_ids=natal.trace_ids + (f"TR-P7-NAR-{domain_id}",),
                confidence=natal.confidence,
                domain=domain_id,
            )
        )
    return tuple(items)


def _luck_blocks(facts: NarrativeComposerFacts, used: set[str]) -> tuple[NarrativeBlock, ...]:
    if facts.luck.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return ()
    items: list[NarrativeBlock] = []
    window = facts.luck.time_window or facts.luck.cycle_id
    if window:
        items.append(
            _block(
                "nar.luck.window",
                "temporal",
                "P1",
                SECTION_TITLES["temporal"],
                LUCK_WINDOW.format(window=window),
                evidence_ids=facts.luck.evidence_ids[:1],
                trace_ids=facts.luck.trace_ids + ("TR-P7-NAR-luck",),
            )
        )
    for domain_id in facts.domain_order:
        luck = facts.luck.items.get(domain_id)
        if luck is None or luck.activation_state.value in {"unresolved", "not_applicable"}:
            continue
        if luck.activation_state.value not in {"overloaded", "peak", "strong", "suppressed", "dormant"}:
            continue
        if f"overload:{domain_id}" in used:
            continue
        used.add(f"overload:{domain_id}")
        items.append(
            _block(
                f"nar.luck.{domain_id}",
                "temporal",
                "P1",
                domain_title(domain_id),
                OVERLOAD_TEMPLATE.format(
                    domain=domain_title(domain_id),
                    state=luck_state_label(luck.activation_state.value),
                ),
                evidence_ids=luck.evidence_ids[:1],
                trace_ids=luck.trace_ids + ("TR-P7-NAR-luck",),
                domain=domain_id,
            )
        )
    for finding in facts.interaction.findings[:4]:
        relation = interaction_label(finding.interaction_type)
        if not relation:
            continue
        items.append(
            _block(
                f"nar.luck.ix.{finding.finding_id or finding.interaction_type}",
                "temporal",
                "P1",
                SECTION_TITLES["temporal"],
                INTERACTION_TEMPLATE.format(
                    source=domain_title(finding.source_domain),
                    relation=relation,
                    target=domain_title(finding.target_domain),
                ),
                evidence_ids=finding.evidence_ids[:1],
                trace_ids=finding.trace_ids + ("TR-P7-NAR-luck",),
            )
        )
    year = facts.temporal.time_window
    if year and facts.temporal.status is EvaluationStatus.RESOLVED:
        items.append(
            _block(
                "nar.luck.annual",
                "temporal",
                "P1",
                SECTION_TITLES["temporal"],
                f"{ANNUAL_WINDOW.format(year=year)} {NO_EVENT}",
                evidence_ids=facts.temporal.evidence_ids[:1],
                trace_ids=facts.temporal.trace_ids + ("TR-P7-NAR-annual",),
            )
        )
    situation = situation_label(facts.interaction.life_situation.situation_id)
    if situation:
        items.append(
            _block(
                "nar.luck.situation",
                "temporal",
                "P1",
                SECTION_TITLES["temporal"],
                situation,
                evidence_ids=facts.interaction.evidence_ids[:1],
                trace_ids=("TR-P7-NAR-luck",),
            )
        )
    return tuple(items[:8])


def _action_blocks(facts: NarrativeComposerFacts) -> tuple[NarrativeBlock, ...]:
    if facts.optimization.state in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return ()
    by_id = {item.action_id: item for item in facts.optimization.actions}
    items: list[NarrativeBlock] = []
    for action_id in facts.optimization.top_priorities[:3]:
        action = by_id.get(action_id)
        if action is None:
            continue
        items.append(_action_block(action, f"nar.action.{len(items) + 1}"))
    seen_ids = set(facts.optimization.top_priorities[:3])
    seen_keys = {
        by_id[action_id].recommended_action_key
        for action_id in facts.optimization.top_priorities[:3]
        if action_id in by_id
    }
    natal = next((item for item in facts.optimization.actions if item.time_scope == "natal_long_term"), None)
    annual = next((item for item in facts.optimization.actions if item.time_scope == "current_annual"), None)
    luck = next((item for item in facts.optimization.actions if item.time_scope == "current_luck_cycle"), None)
    for extra in (natal, luck, annual):
        if extra is None or extra.action_id in seen_ids:
            continue
        if extra.recommended_action_key in seen_keys:
            continue
        if len(items) >= 6:
            break
        seen_ids.add(extra.action_id)
        seen_keys.add(extra.recommended_action_key)
        items.append(_action_block(extra, f"nar.action.{len(items) + 1}"))
    return tuple(items)


def _action_block(action: OptimizationAction, block_id: str) -> NarrativeBlock:
    title = action_label(action.recommended_action_key) or action.recommended_action_key
    reason = reason_label(action.reason_key)
    scope = action.time_scope
    summary = f"{title}. {reason}".strip()
    return _block(
        block_id,
        "action",
        action.priority,
        title,
        summary,
        details=(scope,),
        evidence_ids=action.evidence_ids[:3],
        trace_ids=action.trace_ids + ("TR-P7-NAR-action",),
        confidence=action.confidence,
        domain=action.target_domain,
    )


def _closing(actions: tuple[NarrativeBlock, ...]) -> NarrativeBlock:
    parts = [CLOSING_LEAD]
    for item in actions[:3]:
        if item.title and item.title not in parts:
            parts.append(item.title)
    return _block(
        "nar.closing",
        "closing_summary",
        "P1",
        SECTION_TITLES["closing_summary"],
        " ".join(parts),
        evidence_ids=tuple(eid for item in actions for eid in item.evidence_ids[:1]),
        trace_ids=("TR-P7-NAR-closing",),
    )


def _graph(blocks: tuple[NarrativeBlock, ...], facts: NarrativeComposerFacts) -> NarrativeGraph:
    nodes = tuple(
        NarrativeNode(
            node_id=item.block_id,
            node_type=_node_type(item.block_type),
            layer=NarrativeLayer.COMMERCIAL,
            evidence_ids=item.evidence_ids,
            message_key=item.block_id,
        )
        for item in blocks
    )
    by_type: dict[str, list[str]] = {}
    for item in blocks:
        by_type.setdefault(item.block_type, []).append(item.block_id)
    edges: list[NarrativeEdge] = []
    exec_id = by_type.get("executive_summary", [""])[0]
    for kind, edge_type in (
        ("strength", NarrativeEdgeType.SUMMARIZES),
        ("risk", NarrativeEdgeType.SUMMARIZES),
        ("action", NarrativeEdgeType.SUMMARIZES),
    ):
        for target in by_type.get(kind, [])[:3]:
            if exec_id:
                edges.append(NarrativeEdge(exec_id, target, edge_type))
    for strength_id in by_type.get("strength", [])[:1]:
        for domain_id in by_type.get("domain_section", [])[:1]:
            edges.append(NarrativeEdge(strength_id, domain_id, NarrativeEdgeType.EXPLAINS))
    for risk_id in by_type.get("risk", [])[:1]:
        for domain_id in by_type.get("domain_section", []):
            if "wealth" in domain_id or "vitality" in domain_id:
                edges.append(NarrativeEdge(risk_id, domain_id, NarrativeEdgeType.QUALIFIES))
                break
    career = next((item for item in blocks if item.domain == "career" and item.block_type == "domain_section"), None)
    vitality = next((item for item in blocks if item.domain == "vitality" and item.block_type == "domain_section"), None)
    if career and vitality:
        edges.append(NarrativeEdge(career.block_id, vitality.block_id, NarrativeEdgeType.CONTRASTS))
    for action_id in by_type.get("action", [])[:1]:
        for risk_id in by_type.get("risk", [])[:1]:
            edges.append(NarrativeEdge(action_id, risk_id, NarrativeEdgeType.SUPPORTS))
    for temporal_id in by_type.get("temporal", [])[:1]:
        for strength_id in by_type.get("strength", [])[:1]:
            edges.append(NarrativeEdge(temporal_id, strength_id, NarrativeEdgeType.QUALIFIES))
    for domain_id in by_type.get("domain_section", [])[:2]:
        if exec_id:
            edges.append(NarrativeEdge(exec_id, domain_id, NarrativeEdgeType.EXPANDS))
    _ = facts
    return NarrativeGraph(nodes=nodes, edges=tuple(edges), schema_version=SCHEMA_COMPOSER)


def _with_sources(
    blocks: tuple[NarrativeBlock, ...],
    facts: NarrativeComposerFacts,
) -> tuple[NarrativeBlock, ...]:
    fallback = facts.evidence_priority.dominant_evidence[:1] or facts.evidence_priority.evidence_ids[:1]
    if not fallback and facts.snapshot and facts.snapshot.mingju_result_id:
        fallback = (facts.snapshot.mingju_result_id,)
    if not fallback:
        fallback = ("mc01.structure",)
    filled: list[NarrativeBlock] = []
    for item in blocks:
        if item.evidence_ids:
            filled.append(item)
        else:
            filled.append(replace(item, evidence_ids=fallback))
    return tuple(filled)


def _p0_p1(facts: NarrativeComposerFacts) -> tuple[EvidencePriorityFinding, ...]:
    return _ranked(
        [
            item
            for item in facts.evidence_priority.findings
            if item.tier.value in P0_P1 and item.source_kind not in SHEN_SHA_SOURCE_KINDS
        ]
    )


def _ranked(items: list[EvidencePriorityFinding]) -> tuple[EvidencePriorityFinding, ...]:
    return tuple(
        sorted(
            items,
            key=lambda item: (TIER_INDEX.get(item.tier.value, 99), item.rank, item.finding_id),
        )
    )


def _finding_label(finding: EvidencePriorityFinding) -> str:
    label = finding.customer_label.strip()
    if not label or "TR-P7" in label or label.startswith("E-DI-"):
        return ""
    if _CODE_LABEL.search(label):
        return ""
    if finding.source_kind in _IDENTITY_KINDS:
        return ""
    return label


def _top_action(facts: NarrativeComposerFacts) -> OptimizationAction | None:
    if not facts.optimization.top_priorities:
        return None
    by_id = {item.action_id: item for item in facts.optimization.actions}
    return by_id.get(facts.optimization.top_priorities[0])


def _high(finding: EvidencePriorityFinding) -> bool:
    value = finding.confidence.value
    return value is None or value >= HIGH_CONFIDENCE


def _confidence(blocks: tuple[NarrativeBlock, ...]) -> ConfidenceValue:
    values = [item.confidence.value for item in blocks if item.confidence.value is not None]
    if not values:
        return ConfidenceValue(value=0.64, summary="narrative_composer")
    return ConfidenceValue(value=round(sum(values) / len(values), 2), summary="narrative_composer")


def _node_type(block_type: str) -> NarrativeNodeType:
    try:
        return NarrativeNodeType(block_type)
    except ValueError:
        return NarrativeNodeType.SUPPORTING_EVIDENCE


def _block(
    block_id: str,
    block_type: str,
    priority: str,
    title: str,
    summary: str,
    *,
    details: tuple[str, ...] = (),
    evidence_ids: tuple[str, ...] = (),
    trace_ids: tuple[str, ...] = (),
    confidence: ConfidenceValue | None = None,
    domain: str = "",
) -> NarrativeBlock:
    return NarrativeBlock(
        block_id=block_id,
        block_type=block_type,
        priority=priority,
        title=title,
        summary=summary,
        details=details,
        confidence=confidence or ConfidenceValue(value=0.64, summary="narrative_composer"),
        evidence_ids=tuple(item for item in evidence_ids if item),
        trace_ids=tuple(item for item in trace_ids if item),
        domain=domain,
    )
