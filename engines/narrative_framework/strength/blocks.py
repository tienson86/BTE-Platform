"""Shared helpers for Strength narrative blocks."""

from __future__ import annotations

from engines.narrative_framework.strength.models import StrengthNarrativeBlock


def make_block(
    slot: str,
    sentences: tuple[str, ...],
    source_paths: tuple[str, ...],
) -> StrengthNarrativeBlock:
    """Build a present or insufficient block from sentences."""
    ready = bool(sentences)
    return StrengthNarrativeBlock(
        slot=slot,
        sentences=sentences,
        source_paths=source_paths if ready else (),
        available=ready,
        insufficient=not ready,
    )
