"""Shared helpers for Luck narrative blocks."""

from __future__ import annotations

from engines.narrative_framework.luck.models import LuckNarrativeBlock


def make_block(
    slot: str,
    sentences: tuple[str, ...],
    source_paths: tuple[str, ...],
) -> LuckNarrativeBlock:
    """Build a present or insufficient block from sentences."""
    ready = bool(sentences)
    return LuckNarrativeBlock(
        slot=slot,
        sentences=sentences,
        source_paths=source_paths if ready else (),
        available=ready,
        insufficient=not ready,
    )
