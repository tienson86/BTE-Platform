"""Deterministic in-memory index of approved knowledge records."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.knowledge.knowledge_registry import normalize_domain
from engines.narrative_v2.knowledge.knowledge_status import STATUS_APPROVED


@dataclass(frozen=True, slots=True)
class IndexedKnowledge:
    """Normalized approved record. Source copy only."""

    knowledge_id: str
    domain: str
    key: str
    knowledge_type: str
    status: str
    technical_meaning: str | None
    customer_meaning_candidate: str | None
    boundaries: tuple[str, ...]
    recommendations: tuple[str, ...]
    source_path: str
    version: str | None
    aliases: tuple[str, ...]


class KnowledgeIndex:
    """Exact-key index. No fuzzy lookup. No embeddings."""

    def __init__(self, records: tuple[IndexedKnowledge, ...]) -> None:
        self._records = records
        by_domain_key: dict[tuple[str, str], IndexedKnowledge] = {}
        by_semantic: dict[str, list[IndexedKnowledge]] = {}
        by_id: dict[str, IndexedKnowledge] = {}
        for record in records:
            if record.status != STATUS_APPROVED:
                continue
            by_id[record.knowledge_id] = record
            domain = normalize_domain(record.domain)
            keys = (record.key, record.knowledge_id, *record.aliases)
            for key in keys:
                if not key:
                    continue
                slot = (domain, key)
                existing = by_domain_key.get(slot)
                if existing is not None and existing.knowledge_id != record.knowledge_id:
                    continue
                by_domain_key[slot] = record
            if record.knowledge_id:
                by_semantic.setdefault(record.knowledge_id, []).append(record)
        self._by_domain_key = by_domain_key
        self._by_semantic = {key: tuple(vals) for key, vals in by_semantic.items()}
        self._by_id = by_id

    def records(self) -> tuple[IndexedKnowledge, ...]:
        """Return approved records in load order."""
        return self._records

    def get(self, domain: str, key: str) -> IndexedKnowledge | None:
        """Exact domain+key lookup, including documented aliases."""
        return self._by_domain_key.get((normalize_domain(domain), key))

    def get_by_id(self, knowledge_id: str) -> IndexedKnowledge | None:
        """Exact knowledge_id lookup."""
        return self._by_id.get(knowledge_id)

    def get_by_semantic_key(self, semantic_key: str) -> tuple[IndexedKnowledge, ...]:
        """Exact semantic_key lookup. Empty when none is published."""
        return self._by_semantic.get(semantic_key, ())

    def versions(self) -> tuple[tuple[str, str | None], ...]:
        """Return stable (knowledge_id, version) pairs."""
        return tuple(
            (record.knowledge_id, record.version)
            for record in sorted(self._records, key=lambda item: item.knowledge_id)
        )
