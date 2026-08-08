"""Tone Resolver — Sprint C tone metadata (no prose rewriting)."""

from __future__ import annotations

from engines.narrative_engine.runtime.models import ComponentType

from .constants import COMPONENT_TONES


class ToneResolver:
    """Resolve component tone labels from the writing system."""

    def resolve(self, component_type: ComponentType) -> str:
        """Return tone key for a component."""
        return COMPONENT_TONES.get(component_type.value, "neutral_factual")
