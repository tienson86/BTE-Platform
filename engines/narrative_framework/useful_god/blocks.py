"""Shared helpers for Useful God narrative blocks."""

from __future__ import annotations

from engines.narrative_framework.useful_god.models import UsefulGodNarrativeBlock


def make_block(
    slot: str,
    sentences: tuple[str, ...],
    source_paths: tuple[str, ...],
) -> UsefulGodNarrativeBlock:
    """Build a present or insufficient block from sentences."""
    ready = bool(sentences)
    return UsefulGodNarrativeBlock(
        slot=slot,
        sentences=sentences,
        source_paths=source_paths if ready else (),
        available=ready,
        insufficient=not ready,
    )
