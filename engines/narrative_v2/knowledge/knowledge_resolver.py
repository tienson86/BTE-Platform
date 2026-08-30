"""Knowledge Resolver — ReasoningContext → NarrativeKnowledgeContext.

Matches approved knowledge. Does not rewrite. Does not invent.
"""

from __future__ import annotations

import logging

from engines.narrative_v2.evidence.evidence_context import NarrativeEvidenceContext
from engines.narrative_v2.evidence.evidence_item import STATUS_AVAILABLE
from engines.narrative_v2.knowledge.knowledge_context import (
    KnowledgeContractGap,
    KnowledgeMatch,
    KnowledgeUnresolved,
    NarrativeKnowledgeContext,
)
from engines.narrative_v2.knowledge.knowledge_errors import KnowledgeError
from engines.narrative_v2.knowledge.knowledge_index import IndexedKnowledge, KnowledgeIndex
from engines.narrative_v2.knowledge.knowledge_item import KnowledgeItem
from engines.narrative_v2.knowledge.knowledge_loader import KnowledgeLoader
from engines.narrative_v2.knowledge.knowledge_reference import KnowledgeReference
from engines.narrative_v2.knowledge.knowledge_registry import (
    KnowledgeRegistry,
    TARGET_SEMANTIC_KEYS,
)
from engines.narrative_v2.knowledge.knowledge_status import (
    PARTIAL,
    REASON_NO_APPROVED_KNOWLEDGE,
    REASON_SOURCE_NOT_APPROVED,
    REASON_UNSUPPORTED_SEMANTIC_KEY,
    RESOLVED,
    RESOLVER_VERSION,
    STATUS_APPROVED,
    UNRESOLVED,
)
from engines.narrative_v2.knowledge.knowledge_validator import KnowledgeValidator
from engines.narrative_v2.reasoning.reasoning_context import NarrativeReasoningContext
from engines.narrative_v2.reasoning.reasoning_node import KIND_BOUNDARY, ReasoningNode

logger = logging.getLogger(__name__)

_CONTEXT_METADATA: tuple[tuple[str, str], ...] = (
    ("shadow_mode", "true"),
    ("replaces_pack05", "false"),
    ("portal_connected", "false"),
    ("layer", "knowledge"),
    ("resolver_version", RESOLVER_VERSION),
)


class KnowledgeResolver:
    """Approved-knowledge resolution. Shadow mode. No narrative rewrite."""

    def __init__(
        self,
        *,
        index: KnowledgeIndex | None = None,
        registry: KnowledgeRegistry | None = None,
        validator: KnowledgeValidator | None = None,
    ) -> None:
        self._index = index if index is not None else KnowledgeLoader().load_index()
        self._registry = registry or KnowledgeRegistry()
        self._validator = validator or KnowledgeValidator()

    def resolve(
        self,
        reasoning_context: object,
        evidence_context: object | None = None,
    ) -> NarrativeKnowledgeContext:
        """Resolve approved knowledge for reasoning semantics."""
        reasoning = _require_reasoning(reasoning_context)
        evidence = _require_evidence(evidence_context)
        items_by_id: dict[str, KnowledgeItem] = {}
        matches: list[KnowledgeMatch] = []
        unresolved: list[KnowledgeUnresolved] = []
        gaps: list[KnowledgeContractGap] = []
        grouped = _group_target_nodes(reasoning)
        for semantic_key in sorted(grouped):
            nodes = grouped[semantic_key]
            self._resolve_key(
                semantic_key,
                nodes,
                evidence,
                items_by_id,
                matches,
                unresolved,
                gaps,
            )
        items = tuple(sorted(items_by_id.values(), key=lambda item: item.knowledge_id))
        ordered_matches = tuple(
            sorted(matches, key=lambda match: (match.semantic_key, match.knowledge_id))
        )
        ordered_unresolved = tuple(
            sorted(unresolved, key=lambda entry: (entry.semantic_key, entry.reason))
        )
        status = _context_status(items, ordered_unresolved)
        versions = sorted(
            {item.version for item in items if item.version is not None}
        )
        metadata = _CONTEXT_METADATA + tuple(
            ("knowledge_version", version) for version in versions
        )
        context = NarrativeKnowledgeContext(
            items=items,
            matches=ordered_matches,
            unresolved=ordered_unresolved,
            references=tuple(item.references[0] for item in items if item.references),
            metadata=metadata,
            status=status,
            contract_gaps=tuple(gaps),
        )
        self._validator.assert_valid(context, reasoning, evidence)
        return context

    def _resolve_key(
        self,
        semantic_key: str,
        nodes: tuple[ReasoningNode, ...],
        evidence: NarrativeEvidenceContext,
        items_by_id: dict[str, KnowledgeItem],
        matches: list[KnowledgeMatch],
        unresolved: list[KnowledgeUnresolved],
        gaps: list[KnowledgeContractGap],
    ) -> None:
        reasoning_ids = tuple(node.reasoning_id for node in nodes)
        evidence_ids = _unique_ids(eid for node in nodes for eid in node.evidence_ids)
        exact = self._index.get_by_semantic_key(semantic_key)
        if exact:
            for record in exact:
                self._accept(record, semantic_key, reasoning_ids, evidence_ids, items_by_id, matches, gaps)
            return
        aliased = self._registry.alias_of(semantic_key)
        if aliased != semantic_key:
            aliased_hits = self._index.get_by_semantic_key(aliased)
            if aliased_hits:
                for record in aliased_hits:
                    self._accept(
                        record, semantic_key, reasoning_ids, evidence_ids, items_by_id, matches, gaps
                    )
                return
        lookups = self._registry.lookups(semantic_key)
        if not lookups:
            unresolved.append(
                KnowledgeUnresolved(
                    semantic_key=semantic_key,
                    reason=REASON_UNSUPPORTED_SEMANTIC_KEY,
                    required_source="",
                    reasoning_ids=reasoning_ids,
                    evidence_ids=evidence_ids,
                )
            )
            return
        found = False
        last_source = lookups[0].required_source
        for lookup in lookups:
            last_source = lookup.required_source
            keys = _evidence_keys(evidence, lookup.evidence_ids)
            evidence_ids = _unique_ids((*evidence_ids, *lookup.evidence_ids))
            for key in keys:
                record = self._index.get(lookup.domain, key)
                if record is None:
                    continue
                if record.status != STATUS_APPROVED:
                    unresolved.append(
                        KnowledgeUnresolved(
                            semantic_key=semantic_key,
                            reason=REASON_SOURCE_NOT_APPROVED,
                            required_source=record.source_path,
                            reasoning_ids=reasoning_ids,
                            evidence_ids=evidence_ids,
                        )
                    )
                    continue
                self._accept(
                    record, semantic_key, reasoning_ids, evidence_ids, items_by_id, matches, gaps
                )
                found = True
        if not found:
            unresolved.append(
                KnowledgeUnresolved(
                    semantic_key=semantic_key,
                    reason=REASON_NO_APPROVED_KNOWLEDGE,
                    required_source=last_source,
                    reasoning_ids=reasoning_ids,
                    evidence_ids=evidence_ids,
                )
            )
            logger.debug("Unresolved semantic key %s", semantic_key)

    def _accept(
        self,
        record: IndexedKnowledge,
        semantic_key: str,
        reasoning_ids: tuple[str, ...],
        evidence_ids: tuple[str, ...],
        items_by_id: dict[str, KnowledgeItem],
        matches: list[KnowledgeMatch],
        gaps: list[KnowledgeContractGap],
    ) -> None:
        if record.version is None:
            gaps.append(
                KnowledgeContractGap(
                    field=record.knowledge_id,
                    reason="KNOWLEDGE CONTRACT GAP: source does not publish version",
                )
            )
        if record.knowledge_id not in items_by_id:
            items_by_id[record.knowledge_id] = _item_from_record(
                record, semantic_key, reasoning_ids, evidence_ids
            )
        matches.append(
            KnowledgeMatch(
                semantic_key=semantic_key,
                knowledge_id=record.knowledge_id,
                source=record.source_path,
                status=record.status,
                version=record.version,
                resolution_status=RESOLVED,
                reasoning_ids=reasoning_ids,
                evidence_ids=evidence_ids,
            )
        )


def _require_reasoning(value: object) -> NarrativeReasoningContext:
    if isinstance(value, NarrativeReasoningContext):
        return value
    raise KnowledgeError("Knowledge Resolver accepts NarrativeReasoningContext only")


def _require_evidence(value: object | None) -> NarrativeEvidenceContext:
    if isinstance(value, NarrativeEvidenceContext):
        return value
    raise KnowledgeError("Knowledge Resolver requires NarrativeEvidenceContext for source matching")


def _group_target_nodes(
    reasoning: NarrativeReasoningContext,
) -> dict[str, tuple[ReasoningNode, ...]]:
    grouped: dict[str, list[ReasoningNode]] = {}
    for node in reasoning.nodes:
        if node.semantic_key not in TARGET_SEMANTIC_KEYS and node.kind != KIND_BOUNDARY:
            continue
        grouped.setdefault(node.semantic_key, []).append(node)
    return {key: tuple(nodes) for key, nodes in grouped.items()}


def _evidence_keys(
    evidence: NarrativeEvidenceContext,
    evidence_ids: tuple[str, ...],
) -> tuple[str, ...]:
    keys: list[str] = []
    seen: set[str] = set()
    for evidence_id in evidence_ids:
        item = evidence.item(evidence_id)
        if item is None or item.status != STATUS_AVAILABLE or item.value is None:
            continue
        for key in _scalar_keys(item.value):
            if key in seen:
                continue
            seen.add(key)
            keys.append(key)
    return tuple(keys)


def _scalar_keys(value: object) -> tuple[str, ...]:
    if isinstance(value, tuple):
        return tuple(str(part) for part in value if part not in (None, ""))
    if isinstance(value, (str, int, float, bool)):
        text = str(value).strip()
        return (text,) if text else ()
    return ()


def _unique_ids(values: tuple[str, ...] | object) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:  # type: ignore[union-attr]
        if not isinstance(value, str) or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return tuple(ordered)


def _item_from_record(
    record: IndexedKnowledge,
    semantic_key: str,
    reasoning_ids: tuple[str, ...],
    evidence_ids: tuple[str, ...],
) -> KnowledgeItem:
    reference = KnowledgeReference(
        source_path=record.source_path,
        knowledge_id=record.knowledge_id,
        version=record.version,
        status=record.status,
        reasoning_ids=reasoning_ids,
        evidence_ids=evidence_ids,
    )
    return KnowledgeItem(
        knowledge_id=record.knowledge_id,
        domain=record.domain,
        semantic_key=semantic_key,
        knowledge_type=record.knowledge_type,
        status=record.status,
        technical_meaning=record.technical_meaning,
        customer_meaning_candidate=record.customer_meaning_candidate,
        boundaries=record.boundaries,
        recommendations=record.recommendations,
        references=(reference,),
        source_path=record.source_path,
        version=record.version,
        metadata=(("resolver_version", RESOLVER_VERSION),),
    )


def _context_status(
    items: tuple[KnowledgeItem, ...],
    unresolved: tuple[KnowledgeUnresolved, ...],
) -> str:
    if items and unresolved:
        return PARTIAL
    if items:
        return RESOLVED
    return UNRESOLVED
