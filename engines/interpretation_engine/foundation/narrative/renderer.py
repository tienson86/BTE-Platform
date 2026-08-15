"""Narrative Renderer — organize copied language into canonical sections."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.constants import (
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
from engines.interpretation_engine.foundation.narrative.text import fingerprint

_SECTION_CAP = 8


def render_sections(
    *,
    graph: EvidenceGraph,
    chains: tuple[ReasoningChain, ...],
    applications: tuple[ApplicationItem, ...],
    recommendations: tuple[RecommendationItem, ...],
    warnings: tuple[WarningItem, ...],
) -> tuple[tuple[NarrativeSection, ...], tuple[TraceabilityRecord, ...]]:
    """Render seven sections. Repeated ideas are dropped, not rewritten."""
    used: set[str] = set()
    by_name: dict[str, list[NarrativeSentence]] = {name: [] for name in NARRATIVE_SECTIONS}
    _render_summary(graph, by_name, used)
    _render_observations(graph, by_name, used)
    _render_reasoning(chains, graph, by_name, used)
    _render_impacts(applications, graph, by_name, used)
    _render_recommendations(recommendations, graph, by_name, used)
    _render_warnings(warnings, graph, by_name, used)
    _render_conclusions(graph, by_name, used)
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
    traces = _traceability(sections, graph)
    return sections, traces


def _render_summary(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Executive Summary uses summary-slot conclusions and facts."""
    section = SECTION_EXECUTIVE_SUMMARY
    candidates = [
        node
        for node in graph.nodes
        if SLOT_TO_SECTION.get(node.slot) == section
    ]
    _append_nodes(section, candidates, graph, by_name, used)


def _render_observations(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Observation uses copied facts and evidence."""
    candidates = [
        node
        for node in graph.nodes
        if SLOT_TO_SECTION.get(node.slot) == SECTION_OBSERVATION
    ]
    _append_nodes(SECTION_OBSERVATION, candidates, graph, by_name, used)


def _render_reasoning(
    chains: tuple[ReasoningChain, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Reasoning renders structured chains as copied reason then conclusion."""
    for chain in chains:
        text = chain.reason
        if fingerprint(text) in used:
            continue
        evidence_ids = tuple(
            dict.fromkeys([*chain.fact_ids, *chain.evidence_ids, chain.reason_id])
        )
        sentence = _sentence(
            SECTION_REASONING,
            len(by_name[SECTION_REASONING]),
            text,
            evidence_ids,
            graph,
        )
        if sentence is None:
            continue
        used.add(fingerprint(text))
        by_name[SECTION_REASONING].append(sentence)
        if len(by_name[SECTION_REASONING]) >= _SECTION_CAP:
            break


def _render_impacts(
    applications: tuple[ApplicationItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Impact maps implications; it does not predict outcomes."""
    for item in applications:
        text = f"{item.customer_domain}: {item.statement}"
        if fingerprint(item.statement) in used or fingerprint(text) in used:
            continue
        sentence = _sentence(
            SECTION_IMPACT,
            len(by_name[SECTION_IMPACT]),
            text,
            item.evidence_ids,
            graph,
        )
        if sentence is None:
            continue
        used.add(fingerprint(item.statement))
        used.add(fingerprint(text))
        by_name[SECTION_IMPACT].append(sentence)
        if len(by_name[SECTION_IMPACT]) >= _SECTION_CAP:
            break


def _render_recommendations(
    recommendations: tuple[RecommendationItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Recommendation section copies structured actions with evidence."""
    for item in recommendations:
        if fingerprint(item.action) in used:
            continue
        sentence = _sentence(
            SECTION_RECOMMENDATION,
            len(by_name[SECTION_RECOMMENDATION]),
            item.action,
            item.evidence_ids,
            graph,
        )
        if sentence is None:
            continue
        used.add(fingerprint(item.action))
        by_name[SECTION_RECOMMENDATION].append(sentence)
        if len(by_name[SECTION_RECOMMENDATION]) >= _SECTION_CAP:
            break


def _render_warnings(
    warnings: tuple[WarningItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Warning section copies risks; mitigation is appended when already present."""
    for item in warnings:
        if fingerprint(item.risk) in used:
            continue
        text = item.risk
        if item.mitigation:
            text = f"{item.risk} {item.mitigation}"
        sentence = _sentence(
            SECTION_WARNING,
            len(by_name[SECTION_WARNING]),
            text,
            item.evidence_ids,
            graph,
        )
        if sentence is None:
            continue
        used.add(fingerprint(item.risk))
        by_name[SECTION_WARNING].append(sentence)
        if len(by_name[SECTION_WARNING]) >= _SECTION_CAP:
            break


def _render_conclusions(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Conclusion uses remaining conclusion-slot statements."""
    candidates = [
        node
        for node in graph.nodes
        if SLOT_TO_SECTION.get(node.slot) == SECTION_CONCLUSION
    ]
    _append_nodes(SECTION_CONCLUSION, candidates, graph, by_name, used)


def _append_nodes(
    section: str,
    candidates: list[EvidenceNode],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    used: set[str],
) -> None:
    """Append unique copied statements, keeping one reserved sentence if needed."""
    for node in candidates:
        if len(by_name[section]) >= _SECTION_CAP:
            break
        mark = fingerprint(node.statement)
        if mark in used and by_name[section]:
            continue
        sentence = _sentence(
            section,
            len(by_name[section]),
            node.statement,
            (node.evidence_id, *node.alias_ids),
            graph,
        )
        if sentence is None:
            continue
        used.add(mark)
        by_name[section].append(sentence)


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
