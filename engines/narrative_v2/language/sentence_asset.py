"""SentenceAsset — one approved customer-language unit."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SentenceReference:
    """Trace from a sentence asset to approved knowledge."""

    knowledge_id: str
    source_path: str


@dataclass(frozen=True, slots=True)
class SentenceAsset:
    """How to say an already-approved Meaning. Not new astrology knowledge."""

    sentence_id: str
    semantic_key: str
    domain: str
    category: str
    meaning_key: str
    text: str
    locale: str
    audience: str
    style: str
    status: str
    priority: int
    source_knowledge_ids: tuple[str, ...]
    references: tuple[SentenceReference, ...]
    version: str
    metadata: tuple[tuple[str, str], ...] = ()
