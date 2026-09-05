"""Merge evidence that refers to the same semantic cause."""

from __future__ import annotations

from engines.detailed_interpretation_engine.evidence_priority.candidates import (
    EvidenceCandidate,
    merge_candidates,
)


def merge_semantic_candidates(items: list[EvidenceCandidate]) -> list[EvidenceCandidate]:
    """Collapse duplicate semantic keys. Preserve traces and source refs."""
    merged: dict[str, EvidenceCandidate] = {}
    order: list[str] = []
    for item in items:
        key = item.semantic_key
        existing = merged.get(key)
        if existing is None:
            merged[key] = item
            order.append(key)
            continue
        merged[key] = merge_candidates(existing, item)
    return [merged[key] for key in order]
