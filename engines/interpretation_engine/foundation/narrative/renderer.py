"""Narrative Renderer — rank and group copied language. No fixed sentence budget."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAINS,
    NARRATIVE_SECTIONS,
    SECTION_CONCLUSION,
    SECTION_EXECUTIVE_SUMMARY,
    SECTION_IMPACT,
    SECTION_OBSERVATION,
    SECTION_REASONING,
    SECTION_RECOMMENDATION,
    SECTION_WARNING,
    SLOT_TO_SECTION,
)
from engines.interpretation_engine.foundation.narrative.mapping import (
    customer_relevance,
    keep_ranked,
    narrative_topic,
    rank_key,
    rank_score,
)
from engines.interpretation_engine.foundation.narrative.models import (
    ApplicationItem,
    EvidenceGraph,
    EvidenceNode,
    NarrativeSection,
    NarrativeSentence,
    RecommendationItem,
    ReasoningChain,
    TraceabilityRecord,
    WarningItem,
)
from engines.interpretation_engine.foundation.narrative.text import (
    fingerprint,
    is_customer_prose,
)


def render_sections(
    *,
    graph: EvidenceGraph,
    chains: tuple[ReasoningChain, ...],
    applications: tuple[ApplicationItem, ...],
    recommendations: tuple[RecommendationItem, ...],
    warnings: tuple[WarningItem, ...],
) -> tuple[tuple[NarrativeSection, ...], tuple[TraceabilityRecord, ...]]:
    """Render seven sections. Repeated evidence is dropped, not rewritten."""
    by_name: dict[str, list[NarrativeSentence]] = {name: [] for name in NARRATIVE_SECTIONS}
    _render_summary(graph, by_name)
    _render_observations(graph, by_name)
    _render_reasoning(chains, graph, by_name)
    _render_impacts(applications, graph, by_name)
    _render_recommendations(recommendations, graph, by_name)
    _render_warnings(warnings, graph, by_name)
    _render_conclusions(graph, by_name)
    sections = tuple(
        NarrativeSection(
            name=name,
            sentences=tuple(by_name[name]),
            evidence_ids=tuple(
                dict.fromkeys(
                    evidence_id
                    for sentence in by_name[name]
                    for evidence_id in sentence.evidence_ids
                )
            ),
        )
        for name in NARRATIVE_SECTIONS
    )
    return sections, _traceability(sections, graph)


def _render_summary(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Executive Summary uses ranked summary-slot evidence."""
    candidates = [
        node
        for node in _ranked_nodes(graph)
        if SLOT_TO_SECTION.get(node.slot) == SECTION_EXECUTIVE_SUMMARY
    ]
    _append_nodes(SECTION_EXECUTIVE_SUMMARY, candidates, graph, by_name)


def _render_observations(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Observation uses copied facts and evidence, unique by evidence id."""
    candidates = [
        node
        for node in _ranked_nodes(graph)
        if SLOT_TO_SECTION.get(node.slot) == SECTION_OBSERVATION
    ]
    _append_nodes(SECTION_OBSERVATION, candidates, graph, by_name)


def _render_reasoning(
    chains: tuple[ReasoningChain, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Reasoning is grouped by customer topic, not by engine."""
    grouped: dict[str, list[ReasoningChain]] = {topic: [] for topic in CUSTOMER_DOMAINS}
    seen_reasons: set[str] = set()
    for chain in _ranked_chains(chains, graph):
        if chain.reason_id in seen_reasons:
            continue
        topic = chain.topic if chain.topic in CUSTOMER_DOMAINS else ""
        if not topic:
            continue
        grouped[topic].append(chain)
        seen_reasons.add(chain.reason_id)
    for topic in CUSTOMER_DOMAINS:
        topic_chains = keep_ranked(
            grouped[topic],
            lambda item, current_graph=graph: _chain_score(item, current_graph),
        )
        if not topic_chains:
            continue
        text = _topic_reasoning_text(topic, topic_chains)
        if not is_customer_prose(text.split(":", 1)[-1]):
            continue
        evidence_ids = tuple(
            dict.fromkeys(
                evidence_id
                for chain in topic_chains
                for evidence_id in (*chain.fact_ids, *chain.evidence_ids, chain.reason_id)
            )
        )
        sentence = _sentence(
            SECTION_REASONING,
            len(by_name[SECTION_REASONING]),
            text,
            evidence_ids,
            graph,
        )
        if sentence is not None:
            by_name[SECTION_REASONING].append(sentence)


def _render_impacts(
    applications: tuple[ApplicationItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Impact groups implications by customer topic. It does not predict outcomes."""
    grouped: dict[str, list[ApplicationItem]] = {topic: [] for topic in CUSTOMER_DOMAINS}
    used_local: set[str] = set()
    ranked = sorted(
        applications,
        key=lambda item: rank_key(
            item.domain,
            item.importance,
            item.confidence,
            customer_relevance(item.customer_domain),
        ),
        reverse=True,
    )
    for item in ranked:
        if item.customer_domain not in CUSTOMER_DOMAINS:
            continue
        if not is_customer_prose(item.statement):
            continue
        if used_local.intersection(item.evidence_ids) and grouped[item.customer_domain]:
            continue
        grouped[item.customer_domain].append(item)
        used_local.update(item.evidence_ids)
    for topic in CUSTOMER_DOMAINS:
        items = keep_ranked(
            grouped[topic],
            lambda item: rank_score(
                item.domain,
                item.importance,
                item.confidence,
                customer_relevance(item.customer_domain),
            ),
        )
        if not items:
            continue
        statements = tuple(
            dict.fromkeys(item.statement for item in items if item.statement)
        )
        text = f"{topic}: " + " ".join(statements)
        evidence_ids = tuple(
            dict.fromkeys(evidence_id for item in items for evidence_id in item.evidence_ids)
        )
        sentence = _sentence(
            SECTION_IMPACT,
            len(by_name[SECTION_IMPACT]),
            text,
            evidence_ids,
            graph,
        )
        if sentence is not None:
            by_name[SECTION_IMPACT].append(sentence)


def _render_recommendations(
    recommendations: tuple[RecommendationItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Recommendation section groups unique-by-evidence actions by topic."""
    grouped: dict[str, list[RecommendationItem]] = {topic: [] for topic in CUSTOMER_DOMAINS}
    ranked = sorted(
        recommendations,
        key=lambda item: rank_key(
            item.domain,
            item.importance,
            item.confidence,
            customer_relevance(item.customer_domain),
        ),
        reverse=True,
    )
    seen_ids: set[str] = set()
    seen_actions: set[str] = set()
    for item in ranked:
        topic = narrative_topic(item.customer_domain, item.domain)
        if topic not in CUSTOMER_DOMAINS or not is_customer_prose(item.action):
            continue
        if seen_ids.intersection(item.evidence_ids):
            continue
        mark = fingerprint(item.action)
        if mark in seen_actions:
            continue
        grouped[topic].append(item)
        seen_ids.update(item.evidence_ids)
        seen_actions.add(mark)
    for topic in CUSTOMER_DOMAINS:
        items = keep_ranked(
            grouped[topic],
            lambda item: rank_score(
                item.domain,
                item.importance,
                item.confidence,
                customer_relevance(item.customer_domain),
            ),
        )
        if not items:
            continue
        text = f"{topic}: " + " ".join(dict.fromkeys(item.action for item in items))
        evidence_ids = tuple(
            dict.fromkeys(evidence_id for item in items for evidence_id in item.evidence_ids)
        )
        sentence = _sentence(
            SECTION_RECOMMENDATION,
            len(by_name[SECTION_RECOMMENDATION]),
            text,
            evidence_ids,
            graph,
        )
        if sentence is not None:
            by_name[SECTION_RECOMMENDATION].append(sentence)


def _render_warnings(
    warnings: tuple[WarningItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Warning section groups unique-by-evidence risks by topic."""
    grouped: dict[str, list[WarningItem]] = {topic: [] for topic in CUSTOMER_DOMAINS}
    ranked = sorted(
        warnings,
        key=lambda item: rank_key(item.domain, item.importance, item.confidence, 0.5),
        reverse=True,
    )
    seen_ids: set[str] = set()
    seen_risks: set[str] = set()
    for item in ranked:
        topic = narrative_topic("", item.domain)
        if topic not in CUSTOMER_DOMAINS or not is_customer_prose(item.risk):
            continue
        if seen_ids.intersection(item.evidence_ids):
            continue
        mark = fingerprint(item.risk)
        if mark in seen_risks:
            continue
        grouped[topic].append(item)
        seen_ids.update(item.evidence_ids)
        seen_risks.add(mark)
    for topic in CUSTOMER_DOMAINS:
        items = keep_ranked(
            grouped[topic],
            lambda item: rank_score(item.domain, item.importance, item.confidence, 0.5),
        )
        if not items:
            continue
        parts = []
        for item in items:
            text = item.risk
            if item.mitigation:
                text = f"{item.risk} {item.mitigation}"
            parts.append(text)
        sentence = _sentence(
            SECTION_WARNING,
            len(by_name[SECTION_WARNING]),
            f"{topic}: " + " ".join(dict.fromkeys(parts)),
            tuple(dict.fromkeys(eid for item in items for eid in item.evidence_ids)),
            graph,
        )
        if sentence is not None:
            by_name[SECTION_WARNING].append(sentence)


def _render_conclusions(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Conclusion uses remaining conclusion-slot statements unique by evidence."""
    candidates = [
        node
        for node in _ranked_nodes(graph)
        if SLOT_TO_SECTION.get(node.slot) == SECTION_CONCLUSION
    ]
    _append_nodes(SECTION_CONCLUSION, candidates, graph, by_name)


def _append_nodes(
    section: str,
    candidates: list[EvidenceNode],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Append topic paragraphs from ranked prose. Length follows coverage, not a cap."""
    grouped: dict[str, list[EvidenceNode]] = {topic: [] for topic in CUSTOMER_DOMAINS}
    seen: set[str] = set()
    for node in candidates:
        if not is_customer_prose(node.statement):
            continue
        evidence_ids = (node.evidence_id, *node.alias_ids)
        if seen.intersection(evidence_ids) and grouped.get(
            narrative_topic(node.customer_domain, node.domain, node.engine_truth_ref),
            [],
        ):
            continue
        topic = narrative_topic(node.customer_domain, node.domain, node.engine_truth_ref)
        if topic not in CUSTOMER_DOMAINS:
            continue
        grouped[topic].append(node)
        seen.update(evidence_ids)
    for topic in CUSTOMER_DOMAINS:
        nodes = keep_ranked(grouped[topic], _node_score)
        if not nodes:
            continue
        text = f"{topic}: " + " ".join(dict.fromkeys(node.statement for node in nodes))
        evidence_ids = tuple(
            dict.fromkeys(
                evidence_id
                for node in nodes
                for evidence_id in (node.evidence_id, *node.alias_ids)
            )
        )
        sentence = _sentence(section, len(by_name[section]), text, evidence_ids, graph)
        if sentence is not None:
            by_name[section].append(sentence)


def _ranked_nodes(graph: EvidenceGraph) -> list[EvidenceNode]:
    """Order evidence by importance, confidence, relevance, and bundle priority."""
    return sorted(
        graph.nodes,
        key=lambda node: rank_key(
            node.domain,
            node.importance,
            node.confidence,
            customer_relevance(node.customer_domain, node.engine_truth_ref),
        ),
        reverse=True,
    )


def _ranked_chains(
    chains: tuple[ReasoningChain, ...],
    graph: EvidenceGraph,
) -> list[ReasoningChain]:
    """Order reasoning chains with the same ranking rules."""
    return sorted(chains, key=lambda chain: _chain_score(chain, graph), reverse=True)


def _topic_reasoning_text(topic: str, chains: list[ReasoningChain]) -> str:
    """Organize copied reason/conclusion text under one customer topic."""
    parts: list[str] = []
    seen: set[str] = set()
    for chain in chains:
        for piece in (chain.reason, chain.conclusion):
            if not is_customer_prose(piece):
                continue
            mark = piece.casefold().strip()
            if not mark or mark in seen:
                continue
            seen.add(mark)
            parts.append(piece)
    return f"{topic}: " + " ".join(parts)


def _node_score(node: EvidenceNode) -> float:
    """Coverage score for one evidence node."""
    return rank_score(
        node.domain,
        node.importance,
        node.confidence,
        customer_relevance(node.customer_domain, node.engine_truth_ref),
    )


def _chain_score(chain: ReasoningChain, graph: EvidenceGraph) -> float:
    """Coverage score for one reasoning chain."""
    node = graph.get(chain.reason_id)
    importance = node.importance if node else 0.6
    confidence = node.confidence if node else 0.0
    relevance = customer_relevance(chain.topic, node.engine_truth_ref if node else "")
    return rank_score(chain.domain, importance, confidence, relevance)


def _sentence(
    section: str,
    index: int,
    text: str,
    evidence_ids: tuple[str, ...],
    graph: EvidenceGraph,
) -> NarrativeSentence | None:
    """Build a traceable sentence. Orphan text is rejected."""
    if not text.strip() or not evidence_ids:
        return None
    bundle_ids: list[str] = []
    refs: list[str] = []
    for evidence_id in evidence_ids:
        node = graph.get(evidence_id)
        if node is None:
            continue
        bundle_ids.append(node.bundle_id)
        if node.engine_truth_ref:
            refs.append(node.engine_truth_ref)
    if not bundle_ids:
        return None
    return NarrativeSentence(
        sentence_id=f"s:{section}:{index}",
        section=section,
        text=text,
        evidence_ids=tuple(dict.fromkeys(evidence_ids)),
        bundle_ids=tuple(dict.fromkeys(bundle_ids)),
        engine_truth_refs=tuple(dict.fromkeys(refs)),
    )


def _traceability(
    sections: tuple[NarrativeSection, ...],
    graph: EvidenceGraph,
) -> tuple[TraceabilityRecord, ...]:
    """Index Sentence → Evidence IDs → Bundle → Engine Truth."""
    records: list[TraceabilityRecord] = []
    for section in sections:
        for sentence in section.sentences:
            kinds: list[str] = []
            for evidence_id in sentence.evidence_ids:
                node = graph.get(evidence_id)
                if node is not None:
                    kinds.append(node.bundle_kind)
            records.append(
                TraceabilityRecord(
                    sentence_id=sentence.sentence_id,
                    text=sentence.text,
                    evidence_ids=sentence.evidence_ids,
                    bundle_ids=sentence.bundle_ids,
                    bundle_kinds=tuple(dict.fromkeys(kinds)),
                    engine_truth_refs=sentence.engine_truth_refs,
                )
            )
    return tuple(records)
