"""Build a shared ExportContext from NarrativeV2Presentation. Copy only."""

from __future__ import annotations

from engines.narrative_v2.presentation.presentation_model import (
    ActionPlanPresentation,
    InterpretationPresentation,
    NarrativeV2Presentation,
    OverviewPresentation,
)
from engines.narrative_v2.presentation.presentation_status import PRESENTATION_VERSION

from engines.narrative_v2.export.export_context import ExportBlock, ExportContext
from engines.narrative_v2.export.export_errors import IncompatiblePresentationVersion
from engines.narrative_v2.export.export_serializer import serialize_presentation

OVERVIEW_FIELDS: tuple[str, ...] = (
    "headline",
    "summary",
    "identity",
    "balance",
    "conclusion",
)

INTERPRETATION_FIELDS: tuple[str, ...] = (
    "consulting_flow",
    "overview",
    "observation",
    "reasoning",
    "meaning",
    "impact",
    "recommendation",
    "closing",
)


def build_export_context(presentation: NarrativeV2Presentation) -> ExportContext:
    """Copy Presentation strings into ordered blocks. Does not join or rewrite."""
    version = presentation.metadata.version
    if version != PRESENTATION_VERSION:
        raise IncompatiblePresentationVersion(
            f"expected {PRESENTATION_VERSION}, got {version!r}"
        )
    blocks = (
        *_overview_blocks(presentation.overview),
        *_interpretation_blocks(presentation.interpretation),
        *_action_blocks(presentation.action_plan),
    )
    return ExportContext(
        version=version,
        status=presentation.status,
        language=presentation.metadata.language,
        blocks=blocks,
        presentation=serialize_presentation(presentation),
        shadow_mode=True,
        replaces_pack05=False,
    )


def _overview_blocks(overview: OverviewPresentation | None) -> tuple[ExportBlock, ...]:
    if overview is None:
        return ()
    return tuple(
        ExportBlock(field=f"overview.{name}", text=text)
        for name in OVERVIEW_FIELDS
        if (text := getattr(overview, name))
    )


def _interpretation_blocks(
    interpretation: InterpretationPresentation | None,
) -> tuple[ExportBlock, ...]:
    if interpretation is None:
        return ()
    return tuple(
        ExportBlock(field=f"interpretation.{name}", text=text)
        for name in INTERPRETATION_FIELDS
        if (text := getattr(interpretation, name))
    )


def _action_blocks(plan: ActionPlanPresentation | None) -> tuple[ExportBlock, ...]:
    if plan is None:
        return ()
    rows: list[ExportBlock] = []
    if plan.top_priority is not None:
        rows.extend(_pair("action_plan.top_priority", plan.top_priority.title, plan.top_priority.description))
    for index, item in enumerate(plan.actions):
        rows.extend(_pair(f"action_plan.actions[{index}]", item.title, item.description))
    for index, item in enumerate(plan.warnings):
        rows.extend(_pair(f"action_plan.warnings[{index}]", item.title, item.description))
    if plan.current_period is not None:
        rows.extend(
            _pair(
                "action_plan.current_period",
                plan.current_period.title,
                plan.current_period.description,
            )
        )
    return tuple(rows)


def _pair(prefix: str, title: str, description: str) -> tuple[ExportBlock, ...]:
    blocks: list[ExportBlock] = []
    if title.strip():
        blocks.append(ExportBlock(field=f"{prefix}.title", text=title))
    if description.strip():
        blocks.append(ExportBlock(field=f"{prefix}.description", text=description))
    return tuple(blocks)
