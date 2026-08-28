"""Publish commercial consulting from matched knowledge units.

Orchestration only: matcher then composer. Composer does not rematch.
Does not change Calendar, Bazi, Report HTML, PDF, or DOCX.
"""

from __future__ import annotations

from typing import Any, Mapping

from engines.commercial_composer import (
    CommercialComposerInput,
    compose_commercial_consulting,
)
from engines.consulting_knowledge import match_published_knowledge

_ANALYSIS_KEYS: tuple[str, ...] = (
    "strength",
    "useful_god",
    "pattern",
    "temperature",
    "luck",
    "bazi",
)


def publish_commercial_consulting(
    payload: Mapping[str, Any],
    *,
    identity: Mapping[str, Any] | None = None,
    integrated_narrative: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Match published signals, then compose commercial consulting sections."""
    analysis = _analysis_slice(payload)
    pack = match_published_knowledge(
        analysis_result=analysis,
        identity=identity if identity is not None else payload.get("identity"),
        integrated_narrative=(
            integrated_narrative
            if integrated_narrative is not None
            else payload.get("integrated_narrative")
        ),
    )
    result = compose_commercial_consulting(
        CommercialComposerInput(matched_units=pack.units, analysis=analysis)
    )
    return result.to_dict()


def _analysis_slice(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Copy published analysis fields. Do not recalculate engines."""
    slice_payload: dict[str, Any] = {}
    for key in _ANALYSIS_KEYS:
        value = payload.get(key)
        if isinstance(value, Mapping) and value:
            slice_payload[key] = dict(value)
    return slice_payload
