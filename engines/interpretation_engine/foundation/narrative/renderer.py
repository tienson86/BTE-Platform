"""Narrative Renderer — rank and group copied language. No English topic tags."""

from __future__ import annotations

from dataclasses import replace

from engines.interpretation_engine.foundation.narrative.case_thesis.models import (
    CaseThesisResult,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.relevance import (
    recommendation_matches_thesis,
    warning_matches_thesis,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    CUSTOMER_DOMAIN_CAREER,
    CUSTOMER_DOMAIN_FINANCE,
    CUSTOMER_DOMAIN_HEALTH,
    CUSTOMER_DOMAIN_RELATIONSHIP,
    COMMERCIAL_CONCLUSION_LIMIT,
    COMMERCIAL_IMPACT_PER_DOMAIN,
    COMMERCIAL_OBSERVATION_LIMIT,
    COMMERCIAL_REASONING_LIMIT,
    COMMERCIAL_RECOMMENDATION_LIMIT,
    COMMERCIAL_SUMMARY_LIMIT,
    COMMERCIAL_WARNING_LIMIT,
    GOVERNING_REASONING_DOMAINS,
    IMPACT_CUSTOMER_DOMAINS,
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
from engines.interpretation_engine.foundation.narrative.quality import (
    domain_heading,
    ranked_recommendation_text,
)
from engines.interpretation_engine.foundation.narrative.text import (
    collapse_repeated_disclaimer,
    directive_recommendation,
    fingerprint,
    is_customer_prose,
    strip_engine_level_prefix,
)


def render_sections(
    *,
    graph: EvidenceGraph,
    chains: tuple[ReasoningChain, ...],
    applications: tuple[ApplicationItem, ...],
    recommendations: tuple[RecommendationItem, ...],
    warnings: tuple[WarningItem, ...],
    thesis: CaseThesisResult | None = None,
) -> tuple[tuple[NarrativeSection, ...], tuple[TraceabilityRecord, ...]]:
    """Render seven sections. Repeated evidence is dropped, not rewritten."""
    by_name: dict[str, list[NarrativeSentence]] = {name: [] for name in NARRATIVE_SECTIONS}
    chosen_recs = _choose_recommendations(recommendations, thesis)
    _render_observations(graph, by_name)
    _render_reasoning(chains, graph, by_name, thesis)
    _render_impacts(applications, graph, by_name, thesis)
    _render_recommendations(chosen_recs, graph, by_name)
    _render_warnings(warnings, graph, by_name, thesis)
    _render_summary(graph, by_name, thesis, chosen_recs)
    _render_conclusions(graph, by_name, thesis)
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
    thesis: CaseThesisResult | None = None,
    recommendations: tuple[RecommendationItem, ...] = (),
) -> None:
    """Executive Summary is the whole consultation in at most six sentences."""
    if thesis is not None and thesis.status == "complete":
        parts = _split_sentences(thesis.short_thesis)
        identity = thesis.title.strip()
        governing = parts[0] if parts else ""
        first = f"{identity}. {governing}".strip() if governing else f"{identity}."
        briefing: list[str] = [first]
        for extra in parts[1:3]:
            briefing.append(extra)
        if recommendations:
            action = recommendations[0].action
            if ": " in action:
                action = action.split(": ", 1)[1]
            briefing.append(f"Việc nên làm trước: {action}")
        luck = _luck_frame(graph)
        if luck:
            briefing.append(luck)
        _append_thesis_texts(
            SECTION_EXECUTIVE_SUMMARY,
            tuple(briefing),
            thesis.evidence_ids,
            graph,
            by_name,
            limit=COMMERCIAL_SUMMARY_LIMIT,
        )
        return
    candidates = [
        node
        for node in _ranked_nodes(graph)
        if SLOT_TO_SECTION.get(node.slot) == SECTION_EXECUTIVE_SUMMARY
        and is_customer_prose(node.statement)
    ]
    _append_plain(
        SECTION_EXECUTIVE_SUMMARY,
        candidates[:COMMERCIAL_SUMMARY_LIMIT],
        graph,
        by_name,
    )


def _render_observations(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Observation lists 5–8 current-chart facts. No glossary, no repeated labels."""
    seen: set[str] = set()
    chosen: list[EvidenceNode] = []
    for node in _ranked_nodes(graph):
        if SLOT_TO_SECTION.get(node.slot) != SECTION_OBSERVATION:
            continue
        text = strip_engine_level_prefix(node.statement)
        if not is_customer_prose(text):
            continue
        mark = fingerprint(text)
        if mark in seen:
            continue
        if any(
            mark != prior and (mark.startswith(prior) or prior.startswith(mark))
            for prior in seen
        ):
            continue
        seen.add(mark)
        if text != node.statement:
            node = replace(node, statement=text)
        chosen.append(node)
        if len(chosen) >= COMMERCIAL_OBSERVATION_LIMIT:
            break
    _append_plain(SECTION_OBSERVATION, chosen, graph, by_name)


def _render_reasoning(
    chains: tuple[ReasoningChain, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    thesis: CaseThesisResult | None = None,
) -> None:
    """One synthesis: Pattern + Strength + Useful God as Fact → Reason → Therefore."""
    if thesis is not None and thesis.status == "complete" and thesis.evidence_ids:
        why = (
            f"Nền {thesis.core_pattern} và trạng thái {thesis.core_strength} "
            f"giải thích vì sao hướng chỉnh là {thesis.corrective_direction}."
        )
        _append_thesis_texts(
            SECTION_REASONING,
            (why,),
            thesis.evidence_ids,
            graph,
            by_name,
            limit=1,
        )
    synthesis = _governing_therefore_text(chains, graph)
    if synthesis:
        evidence_ids = tuple(
            dict.fromkeys(
                evidence_id
                for chain in _governing_chains(chains, graph)
                for evidence_id in (*chain.fact_ids, *chain.evidence_ids, chain.reason_id)
            )
        )
        if thesis is not None and thesis.evidence_ids:
            evidence_ids = tuple(dict.fromkeys((*thesis.evidence_ids, *evidence_ids)))
        sentence = _sentence(
            SECTION_REASONING,
            len(by_name[SECTION_REASONING]),
            synthesis,
            evidence_ids,
            graph,
        )
        if sentence is not None:
            by_name[SECTION_REASONING].append(sentence)
    if by_name[SECTION_REASONING]:
        return
    used_marks: set[str] = set()
    for chain in _governing_chains(chains, graph):
        text = _therefore_text(chain, used_marks)
        if not is_customer_prose(text):
            continue
        evidence_ids = tuple(
            dict.fromkeys((*chain.fact_ids, *chain.evidence_ids, chain.reason_id))
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
        if len(by_name[SECTION_REASONING]) >= COMMERCIAL_REASONING_LIMIT:
            break


def _render_impacts(
    applications: tuple[ApplicationItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    thesis: CaseThesisResult | None = None,
) -> None:
    """Impact is one thesis paragraph per life area. Not leftover knowledge."""
    grouped: dict[str, list[ApplicationItem]] = {topic: [] for topic in IMPACT_CUSTOMER_DOMAINS}
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
        if item.customer_domain not in IMPACT_CUSTOMER_DOMAINS:
            continue
        if not is_customer_prose(item.statement):
            continue
        grouped[item.customer_domain].append(item)
    for topic in IMPACT_CUSTOMER_DOMAINS:
        implication = _thesis_implication(thesis, topic)
        items = () if implication else tuple(grouped[topic][:COMMERCIAL_IMPACT_PER_DOMAIN])
        heading = domain_heading(topic)
        if not implication and not items:
            continue
        statements = tuple(dict.fromkeys(item.statement for item in items if item.statement))
        body_parts = [part for part in (implication, *statements) if part]
        body = collapse_repeated_disclaimer(" ".join(body_parts))
        text = f"{heading}: {body}" if heading else body
        evidence_ids = tuple(
            dict.fromkeys(
                [
                    *(thesis.evidence_ids if thesis and implication else ()),
                    *(evidence_id for item in items for evidence_id in item.evidence_ids),
                ]
            )
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


def _choose_recommendations(
    recommendations: tuple[RecommendationItem, ...],
    thesis: CaseThesisResult | None,
) -> tuple[RecommendationItem, ...]:
    """Rank a shortlist of case-specific directives. No ritual Hỷ lists."""
    ranked = sorted(
        recommendations,
        key=lambda item: (
            recommendation_matches_thesis(item, thesis) if thesis else 0.0,
            rank_key(
                item.domain,
                item.importance,
                item.confidence,
                customer_relevance(item.customer_domain),
            ),
        ),
        reverse=True,
    )
    seen_actions: set[str] = set()
    chosen: list[RecommendationItem] = []
    for item in ranked:
        action = directive_recommendation(item.action)
        if not is_customer_prose(action):
            continue
        mark = fingerprint(action)
        if mark in seen_actions:
            continue
        chosen.append(
            RecommendationItem(
                recommendation_id=item.recommendation_id,
                action=action,
                rationale=item.rationale,
                category=item.category,
                evidence_ids=item.evidence_ids,
                bundle_id=item.bundle_id,
                domain=item.domain,
                customer_domain=item.customer_domain,
                confidence=item.confidence,
                importance=item.importance,
            )
        )
        seen_actions.add(mark)
        if len(chosen) >= COMMERCIAL_RECOMMENDATION_LIMIT:
            break
    return tuple(chosen)


def _render_recommendations(
    recommendations: tuple[RecommendationItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Recommendation section exposes a ranked commercial shortlist."""
    for index, item in enumerate(recommendations, start=1):
        sentence = _sentence(
            SECTION_RECOMMENDATION,
            len(by_name[SECTION_RECOMMENDATION]),
            ranked_recommendation_text(index, item.action),
            tuple(dict.fromkeys(item.evidence_ids)),
            graph,
        )
        if sentence is not None:
            by_name[SECTION_RECOMMENDATION].append(sentence)


def _render_warnings(
    warnings: tuple[WarningItem, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    thesis: CaseThesisResult | None = None,
) -> None:
    """Warning section exposes at most three current-chart risks."""
    ranked = sorted(
        warnings,
        key=lambda item: (
            warning_matches_thesis(item, thesis) if thesis else 0.0,
            rank_key(item.domain, item.importance, item.confidence, 0.5),
        ),
        reverse=True,
    )
    seen_ids: set[str] = set()
    seen_risks: set[str] = set()
    chosen: list[WarningItem] = []
    for item in ranked:
        if not is_customer_prose(item.risk):
            continue
        if seen_ids.intersection(item.evidence_ids):
            continue
        mark = fingerprint(item.risk)
        if mark in seen_risks:
            continue
        chosen.append(item)
        seen_ids.update(item.evidence_ids)
        seen_risks.add(mark)
        if len(chosen) >= COMMERCIAL_WARNING_LIMIT:
            break
    for index, item in enumerate(chosen, start=1):
        text = item.risk
        if item.mitigation:
            text = f"{item.risk} {item.mitigation}"
        sentence = _sentence(
            SECTION_WARNING,
            len(by_name[SECTION_WARNING]),
            ranked_recommendation_text(index, text),
            tuple(dict.fromkeys(item.evidence_ids)),
            graph,
        )
        if sentence is not None:
            by_name[SECTION_WARNING].append(sentence)


def _render_conclusions(
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    thesis: CaseThesisResult | None = None,
) -> None:
    """Conclusion is one memorable ending. It does not restart a catalogue."""
    if thesis is not None and thesis.status == "complete":
        closing = (
            f"{thesis.title}: cấu trúc này phù hợp hơn khi {thesis.corrective_direction}. "
            f"Rủi ro tăng khi {thesis.core_tension}. "
            f"Giữ hướng này trên nền {thesis.core_pattern}."
        )
        _append_thesis_texts(
            SECTION_CONCLUSION,
            (closing,),
            thesis.evidence_ids,
            graph,
            by_name,
            limit=1,
        )
        return
    used = {
        fingerprint(sentence.text)
        for name in (
            SECTION_EXECUTIVE_SUMMARY,
            SECTION_REASONING,
            SECTION_IMPACT,
            SECTION_RECOMMENDATION,
            SECTION_CONCLUSION,
        )
        for sentence in by_name[name]
    }
    candidates = [
        node
        for node in _ranked_nodes(graph)
        if SLOT_TO_SECTION.get(node.slot) == SECTION_CONCLUSION
        and is_customer_prose(node.statement)
        and fingerprint(node.statement) not in used
    ]
    _append_plain(
        SECTION_CONCLUSION,
        candidates[:COMMERCIAL_CONCLUSION_LIMIT],
        graph,
        by_name,
    )


def _append_plain(
    section: str,
    candidates: list[EvidenceNode],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
) -> None:
    """Append one sentence per unique fact. No English domain prefix."""
    seen: set[str] = set()
    for node in candidates:
        mark = fingerprint(node.statement)
        if mark in seen:
            continue
        evidence_ids = (node.evidence_id, *node.alias_ids)
        if seen.intersection(evidence_ids):
            continue
        sentence = _sentence(
            section,
            len(by_name[section]),
            node.statement,
            evidence_ids,
            graph,
        )
        if sentence is None:
            continue
        by_name[section].append(sentence)
        seen.add(mark)
        seen.update(evidence_ids)


def _append_thesis_texts(
    section: str,
    texts: tuple[str, ...],
    evidence_ids: tuple[str, ...],
    graph: EvidenceGraph,
    by_name: dict[str, list[NarrativeSentence]],
    *,
    limit: int,
) -> None:
    """Insert thesis spine sentences with existing evidence ids."""
    if not evidence_ids:
        return
    seen = {fingerprint(sentence.text) for sentence in by_name[section]}
    for text in texts:
        if len(by_name[section]) >= limit:
            return
        cleaned = text.strip()
        if not cleaned or not is_customer_prose(cleaned):
            continue
        mark = fingerprint(cleaned)
        if mark in seen:
            continue
        sentence = _sentence(
            section,
            len(by_name[section]),
            cleaned,
            evidence_ids,
            graph,
        )
        if sentence is None:
            continue
        by_name[section].append(sentence)
        seen.add(mark)


def _split_sentences(text: str) -> tuple[str, ...]:
    """Split short thesis into customer sentences."""
    parts = [part.strip() for part in text.replace("? ", ". ").split(". ") if part.strip()]
    cleaned: list[str] = []
    for part in parts:
        item = part if part.endswith((".", "!", "?")) else f"{part}."
        cleaned.append(item)
    return tuple(cleaned)


def _thesis_implication(thesis: CaseThesisResult | None, topic: str) -> str:
    """Copy the matching thesis implication for one life area."""
    if thesis is None or thesis.status != "complete":
        return ""
    mapping = {
        CUSTOMER_DOMAIN_CAREER: thesis.career_implication,
        CUSTOMER_DOMAIN_FINANCE: thesis.finance_implication,
        CUSTOMER_DOMAIN_RELATIONSHIP: thesis.relationship_implication,
        CUSTOMER_DOMAIN_HEALTH: thesis.health_implication,
    }
    return mapping.get(topic, "")


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


def _governing_chains(
    chains: tuple[ReasoningChain, ...],
    graph: EvidenceGraph,
) -> list[ReasoningChain]:
    """Keep Pattern / Strength / Useful God chains only — not a Ten God catalogue."""
    chosen: list[ReasoningChain] = []
    seen: set[str] = set()
    ordered = sorted(
        (chain for chain in chains if chain.domain in GOVERNING_REASONING_DOMAINS),
        key=lambda chain: (
            {"UsefulGod": 0, "Strength": 1, "Pattern": 2}.get(chain.domain, 9),
            -_chain_score(chain, graph),
        ),
    )
    for chain in ordered:
        if chain.domain not in GOVERNING_REASONING_DOMAINS:
            continue
        if chain.reason_id in seen:
            continue
        seen.add(chain.reason_id)
        chosen.append(chain)
    return chosen


def _governing_therefore_text(
    chains: tuple[ReasoningChain, ...],
    graph: EvidenceGraph,
) -> str:
    """Join governing chains into one Fact → Reason → Therefore meaning."""
    used: set[str] = set()
    parts: list[str] = []
    for chain in _governing_chains(chains, graph):
        piece = _therefore_text(chain, used)
        if is_customer_prose(piece):
            parts.append(piece)
        if parts:
            break
    return " ".join(parts)


def _therefore_text(chain: ReasoningChain, seen: set[str]) -> str:
    """Copy fact, reason, and conclusion as one therefore-chain."""
    parts: list[str] = []
    for piece in (chain.fact, chain.reason):
        if not is_customer_prose(piece):
            continue
        mark = fingerprint(piece)
        if not mark or mark in seen:
            continue
        seen.add(mark)
        parts.append(piece)
    conclusion = chain.conclusion
    if is_customer_prose(conclusion):
        mark = fingerprint(conclusion)
        if mark and mark not in seen:
            seen.add(mark)
            if not conclusion.casefold().startswith("vì vậy"):
                conclusion = f"Vì vậy, {conclusion}"
            parts.append(conclusion)
    return " ".join(parts)


def _luck_frame(graph: EvidenceGraph) -> str:
    """Copy the confirmed current Da Yun as a time frame, not a reading."""
    for node in graph.nodes:
        ref = node.engine_truth_ref.casefold()
        if "current_dayun" in ref and is_customer_prose(node.statement):
            if node.statement.startswith("Khung thời gian"):
                return node.statement
    for node in graph.nodes:
        if "current_dayun" in node.engine_truth_ref.casefold() and is_customer_prose(
            node.statement
        ):
            return node.statement
    return ""


def _topic_reasoning_text(chains: list[ReasoningChain], seen: set[str]) -> str:
    """Organize copied reason/conclusion text without English tags."""
    parts: list[str] = []
    for chain in chains:
        for piece in (chain.reason, chain.conclusion):
            if not is_customer_prose(piece):
                continue
            mark = fingerprint(piece)
            if not mark or mark in seen:
                continue
            seen.add(mark)
            parts.append(piece)
    return " ".join(parts)


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
