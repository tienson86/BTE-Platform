"""Traceability pointer for a resolved knowledge item."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KnowledgeReference:
    """Internal trace pointer. Not customer-facing."""

    source_path: str
    knowledge_id: str
    version: str | None
    status: str
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
