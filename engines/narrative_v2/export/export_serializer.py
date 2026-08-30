"""Serialize and hydrate Presentation for export. Copy only."""

from __future__ import annotations

from typing import Any, Mapping

from engines.narrative_v2.presentation.presentation_metadata import PresentationMetadata
from engines.narrative_v2.presentation.presentation_model import (
    ActionItemPresentation,
    ActionPlanPresentation,
    CurrentPeriodPresentation,
    InterpretationPresentation,
    NarrativeV2Presentation,
    OverviewPresentation,
    TopPriorityPresentation,
    WarningPresentation,
)
from engines.narrative_v2.presentation.presentation_serializer import serialize_customer
from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION

from engines.narrative_v2.export.export_errors import IncompatiblePresentationVersion


def serialize_presentation(presentation: NarrativeV2Presentation) -> dict[str, Any]:
    """Canonical customer JSON. Equals Presentation."""
    return serialize_customer(presentation)


def presentation_from_mapping(payload: Mapping[str, Any]) -> NarrativeV2Presentation:
    """Rebuild a Presentation from serialized JSON. Does not invent fields."""
    metadata_raw = _record(payload.get("metadata"))
    version = _text(metadata_raw.get("version") if metadata_raw else None)
    if version != PRESENTATION_VERSION:
        raise IncompatiblePresentationVersion(
            f"expected {PRESENTATION_VERSION}, got {version!r}"
        )
    return NarrativeV2Presentation(
        status=_text(payload.get("status")) or "invalid",
        overview=_overview(_record(payload.get("overview"))),
        interpretation=_interpretation(_record(payload.get("interpretation"))),
        action_plan=_action_plan(_record(payload.get("action_plan"))),
        commercial=None,
        metadata=PresentationMetadata(
            status=_text(metadata_raw.get("status") if metadata_raw else None) or "invalid",
            language=_text(metadata_raw.get("language") if metadata_raw else None) or "vi",
            version=PRESENTATION_VERSION,
            created_at=_text(metadata_raw.get("created_at") if metadata_raw else None)
            or "1970-01-01T00:00:00Z",
        ),
    )


def _overview(raw: dict[str, Any] | None) -> OverviewPresentation | None:
    if raw is None:
        return None
    return OverviewPresentation(
        headline=_text(raw.get("headline")),
        summary=_text(raw.get("summary")),
        identity=_text(raw.get("identity")),
        balance=_text(raw.get("balance")),
        conclusion=_text(raw.get("conclusion")),
    )


def _interpretation(raw: dict[str, Any] | None) -> InterpretationPresentation | None:
    if raw is None:
        return None
    return InterpretationPresentation(
        overview=_text(raw.get("overview")),
        observation=_text(raw.get("observation")),
        reasoning=_text(raw.get("reasoning")),
        meaning=_text(raw.get("meaning")),
        impact=_text(raw.get("impact")),
        recommendation=_text(raw.get("recommendation")),
        closing=_text(raw.get("closing")),
        consulting_flow=_text(raw.get("consulting_flow")),
    )


def _action_plan(raw: dict[str, Any] | None) -> ActionPlanPresentation | None:
    if raw is None:
        return None
    top = _record(raw.get("top_priority"))
    period = _record(raw.get("current_period"))
    actions = raw.get("actions")
    warnings = raw.get("warnings")
    return ActionPlanPresentation(
        top_priority=_titled(top, TopPriorityPresentation),
        actions=tuple(
            ActionItemPresentation(
                title=_text(item.get("title")) or "",
                description=_text(item.get("description")) or "",
                category=_text(item.get("category")) or "",
            )
            for item in _list(actions)
            if isinstance(item, dict)
        ),
        warnings=tuple(
            WarningPresentation(
                title=_text(item.get("title")) or "",
                description=_text(item.get("description")) or "",
            )
            for item in _list(warnings)
            if isinstance(item, dict)
        ),
        current_period=_titled(period, CurrentPeriodPresentation),
    )


def _titled(
    raw: dict[str, Any] | None,
    cls: type[TopPriorityPresentation] | type[CurrentPeriodPresentation],
) -> TopPriorityPresentation | CurrentPeriodPresentation | None:
    if raw is None:
        return None
    return cls(
        title=_text(raw.get("title")) or "",
        description=_text(raw.get("description")) or "",
    )


def _record(value: object) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    return value


def _list(value: object) -> list[object]:
    return list(value) if isinstance(value, list) else []


def _text(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    return value if value.strip() else None
