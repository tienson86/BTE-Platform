"""Freeze a validated Presentation. Mutation is rejected by frozen dataclass."""

from __future__ import annotations

from dataclasses import replace

from engines.narrative_v2.presentation.presentation_model import NarrativeV2Presentation


def freeze(presentation: NarrativeV2Presentation) -> NarrativeV2Presentation:
    """Return an immutable copy. Frozen dataclass rejects later assignment."""
    if not isinstance(presentation, NarrativeV2Presentation):
        raise TypeError("freeze() accepts NarrativeV2Presentation only")
    return replace(presentation)
