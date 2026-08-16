"""Thesis relevance — knowledge enters narrative only if it serves the thesis."""

from __future__ import annotations

from engines.interpretation_engine.foundation.narrative.case_thesis.functions import (
    GOVERNING_DOMAINS,
)
from engines.interpretation_engine.foundation.narrative.case_thesis.models import (
    CaseThesisResult,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_APPLICATION,
    KIND_RECOMMENDATION,
    KIND_WARNING,
)
from engines.interpretation_engine.foundation.narrative.input import (
    ChartFocus,
    CopiedStatement,
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
    RelationshipBundle,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.models import (
    EvidenceGraph,
    EvidenceNode,
    RecommendationItem,
    WarningItem,
)
from engines.interpretation_engine.foundation.narrative.text import fingerprint

_EXCEPTION_MARKERS = ("ngoại lệ", "trừ khi", "không phải lúc nào")


def apply_thesis_relevance(
    source: NarrativeComposerInput,
    thesis: CaseThesisResult,
) -> NarrativeComposerInput:
    """Drop bundle statements that do not serve the current thesis."""
    if thesis.status != "complete":
        return source
    tokens = _thesis_tokens(thesis, source.chart_focus)
    return NarrativeComposerInput(
        decision_bundles=tuple(
            _filter_decision(item, thesis, tokens) for item in source.decision_bundles
        ),
        state_bundles=tuple(
            _filter_state(item, thesis, tokens) for item in source.state_bundles
        ),
        relationship_bundles=tuple(
            _filter_relationship(item, thesis, tokens)
            for item in source.relationship_bundles
        ),
        knowledge_bundles=tuple(
            _filter_knowledge(item, thesis, tokens) for item in source.knowledge_bundles
        ),
        chart_focus=source.chart_focus,
    )


def statement_supports_thesis(
    statement: CopiedStatement,
    thesis: CaseThesisResult,
    tokens: frozenset[str],
    domain: str,
) -> bool:
    """A. support  B. explain  C. exception  D. application tied to thesis."""
    if domain in GOVERNING_DOMAINS:
        return True
    text = fingerprint(statement.text)
    if any(token in text or token in fingerprint(statement.engine_truth_ref) for token in tokens):
        return True
    if statement.kind in {KIND_APPLICATION, KIND_RECOMMENDATION, KIND_WARNING}:
        if any(token in text for token in tokens):
            return True
        if statement.kind == KIND_RECOMMENDATION and thesis.corrective_id:
            return True
        if statement.kind == KIND_WARNING and thesis.tension_id:
            return True
    if any(marker in text for marker in _EXCEPTION_MARKERS):
        return True
    if domain == "ShenSha":
        return False
    return False


def filter_evidence_graph(
    graph: EvidenceGraph,
    thesis: CaseThesisResult,
    focus: ChartFocus | None,
) -> EvidenceGraph:
    """Keep evidence that the thesis stands on or that explains it."""
    if thesis.status != "complete":
        return graph
    tokens = _thesis_tokens(thesis, focus)
    keep = set(thesis.evidence_ids)
    nodes = []
    for node in graph.nodes:
        if node.evidence_id in keep or node.domain in GOVERNING_DOMAINS:
            nodes.append(node)
            continue
        blob = fingerprint(node.statement)
        if any(token in blob for token in tokens):
            nodes.append(node)
    return EvidenceGraph(
        nodes=tuple(nodes),
        raw_count=graph.raw_count,
        merged_count=len(nodes),
    )


def recommendation_matches_thesis(
    item: RecommendationItem,
    thesis: CaseThesisResult | None,
) -> float:
    """Rank boost when an action follows the corrective direction."""
    if thesis is None or thesis.status != "complete":
        return 0.0
    return _match_score(item.action, thesis.corrective_direction, thesis.useful_function)


def warning_matches_thesis(
    item: WarningItem,
    thesis: CaseThesisResult | None,
) -> float:
    """Rank boost when a warning names the core tension."""
    if thesis is None or thesis.status != "complete":
        return 0.0
    blob = f"{item.risk} {item.condition}"
    return _match_score(blob, thesis.core_tension, thesis.ky_function)


def _match_score(text: str, spine: str, function: str) -> float:
    """Cheap overlap score for ranking, not a new model."""
    haystack = fingerprint(text)
    score = 0.0
    for token in fingerprint(spine).split():
        if len(token) > 3 and token in haystack:
            score += 1.0
    if function and function in haystack:
        score += 2.0
    return score


def _thesis_tokens(thesis: CaseThesisResult, focus: ChartFocus | None) -> frozenset[str]:
    """Names and functions the thesis is allowed to talk about."""
    items = [
        thesis.title,
        thesis.core_pattern,
        thesis.core_strength,
        thesis.corrective_id,
        thesis.tension_id,
        *thesis.supporting_facts,
    ]
    if focus is not None:
        items.extend(focus.active_names())
    return frozenset(fingerprint(item) for item in items if item)


def _filter_decision(
    bundle: DecisionBundle,
    thesis: CaseThesisResult,
    tokens: frozenset[str],
) -> DecisionBundle:
    """Keep decision statements that serve the thesis."""
    return DecisionBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        selected=bundle.selected,
        reason=bundle.reason,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, thesis, tokens, bundle.domain),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_state(
    bundle: StateBundle,
    thesis: CaseThesisResult,
    tokens: frozenset[str],
) -> StateBundle:
    """Keep state statements that serve the thesis."""
    return StateBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        state=bundle.state,
        label=bundle.label,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, thesis, tokens, bundle.domain),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_relationship(
    bundle: RelationshipBundle,
    thesis: CaseThesisResult,
    tokens: frozenset[str],
) -> RelationshipBundle:
    """Keep relationship statements that serve the thesis."""
    return RelationshipBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, thesis, tokens, bundle.domain),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_knowledge(
    bundle: KnowledgeBundle,
    thesis: CaseThesisResult,
    tokens: frozenset[str],
) -> KnowledgeBundle:
    """Keep knowledge statements that serve the thesis."""
    return KnowledgeBundle(
        bundle_id=bundle.bundle_id,
        domain=bundle.domain,
        entity_keys=bundle.entity_keys,
        confidence=bundle.confidence,
        importance=bundle.importance,
        statements=_filter_statements(bundle.statements, thesis, tokens, bundle.domain),
        engine_truth_refs=bundle.engine_truth_refs,
    )


def _filter_statements(
    statements: tuple[CopiedStatement, ...],
    thesis: CaseThesisResult,
    tokens: frozenset[str],
    domain: str,
) -> tuple[CopiedStatement, ...]:
    """Apply thesis inclusion policy to one bundle."""
    return tuple(
        item
        for item in statements
        if statement_supports_thesis(item, thesis, tokens, domain)
    )
