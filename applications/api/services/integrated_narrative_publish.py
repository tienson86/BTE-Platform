"""Publish IntegratedNarrative onto Analysis Result.

Consumes the frozen Narrative Platform. Does not change topic engines,
Identity, Report, PDF, or DOCX. Workspace must only read the published dict.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_framework import (
    compose_integrated_narrative,
    compose_luck_narrative,
    compose_pattern_narrative,
    compose_strength_narrative,
    compose_useful_god_narrative,
)


def publish_integrated_narrative(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Compose IntegratedNarrative from published analysis slices.

    Topic composition stays in the frozen Narrative Platform. This publisher
    only attaches the resulting unit onto Analysis Result.
    """
    useful_god = payload.get("useful_god")
    temperature = payload.get("temperature")
    luck = payload.get("_luck_raw") or payload.get("luck")
    unit = compose_integrated_narrative(
        compose_strength_narrative(
            payload.get("strength"),
            useful_god=useful_god,
            temperature=temperature,
        ),
        compose_useful_god_narrative(useful_god),
        compose_pattern_narrative(
            payload.get("pattern"),
            useful_god=useful_god,
            temperature=temperature,
        ),
        compose_luck_narrative(luck),
    )
    return unit.to_dict()
