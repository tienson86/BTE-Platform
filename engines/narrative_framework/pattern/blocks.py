"""Shared helpers for Pattern narrative blocks."""

from __future__ import annotations

from engines.narrative_framework.pattern.models import PatternNarrativeBlock


def make_block(
    slot: str,
    sentences: tuple[str, ...],
    source_paths: tuple[str, ...],
) -> PatternNarrativeBlock:
    """Build a present or insufficient block from sentences."""
    ready = bool(sentences)
    return PatternNarrativeBlock(
        slot=slot,
        sentences=sentences,
        source_paths=source_paths if ready else (),
        available=ready,
        insufficient=not ready,
    )
