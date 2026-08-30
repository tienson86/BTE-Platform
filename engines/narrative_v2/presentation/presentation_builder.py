"""PresentationBuilder — package validated Narrative. Does not create meaning."""

from __future__ import annotations

from engines.narrative_v2.action.action_model import ActionPlanNarrative
from engines.narrative_v2.communication.communication_context import ConsultingNarrative
from engines.narrative_v2.interpretation.interpretation_model import InterpretationNarrative
from engines.narrative_v2.presentation.presentation_errors import PresentationError
from engines.narrative_v2.presentation.presentation_freeze import freeze
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
from engines.narrative_v2.presentation.presentation_status import (
    DEFAULT_LANGUAGE,
    FROZEN_CREATED_AT,
    PRESENTATION_VERSION,
    STATUS_COMPLETE,
    STATUS_INSUFFICIENT,
    STATUS_INVALID,
    STATUS_PARTIAL,
)
from engines.narrative_v2.presentation.presentation_validator import PresentationValidator
from engines.narrative_v2.summary.summary_model import OverviewSummary


class PresentationBuilder:
    """Assemble NarrativeV2Presentation from already-built Narrative objects."""

    def __init__(
        self,
        *,
        validator: PresentationValidator | None = None,
        created_at: str = FROZEN_CREATED_AT,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        self._validator = validator or PresentationValidator()
        self._created_at = created_at
        self._language = language

    def build(
        self,
        overview: object,
        interpretation: object,
        action_plan: object,
        commercial: object = None,
        *,
        consulting: object = None,
    ) -> NarrativeV2Presentation:
        """Copy approved public fields. Reject CanonicalAnalysis and internals."""
        summary = _require_overview(overview)
        narrative = _require_interpretation(interpretation)
        plan = _require_action(action_plan)
        consulting_narrative = _require_consulting(consulting)
        if commercial is not None:
            raise PresentationError("CommercialNarrative is not implemented")
        overview_view = _copy_overview(summary)
        interpretation_view = _copy_interpretation(narrative, consulting_narrative)
        action_view = _copy_action(plan)
        status = _aggregate_status(summary, narrative, plan, overview_view, interpretation_view, action_view)
        presentation = NarrativeV2Presentation(
            status=status,
            overview=overview_view,
            interpretation=interpretation_view,
            action_plan=action_view,
            commercial=None,
            metadata=PresentationMetadata(
                status=status,
                language=self._language,
                version=PRESENTATION_VERSION,
                created_at=self._created_at,
            ),
        )
        self._validator.validate(
            presentation,
            interpretation=narrative,
            consulting=consulting_narrative,
        )
        return freeze(presentation)


def _require_overview(value: object) -> OverviewSummary | None:
    if value is None:
        return None
    if isinstance(value, OverviewSummary):
        return value
    raise PresentationError("PresentationBuilder accepts OverviewSummary only")


def _require_interpretation(value: object) -> InterpretationNarrative | None:
    if value is None:
        return None
    if isinstance(value, InterpretationNarrative):
        return value
    raise PresentationError("PresentationBuilder accepts InterpretationNarrative only")


def _require_action(value: object) -> ActionPlanNarrative | None:
    if value is None:
        return None
    if isinstance(value, ActionPlanNarrative):
        return value
    raise PresentationError("PresentationBuilder accepts ActionPlanNarrative only")


def _require_consulting(value: object) -> ConsultingNarrative | None:
    if value is None:
        return None
    if isinstance(value, ConsultingNarrative):
        return value
    raise PresentationError("PresentationBuilder accepts ConsultingNarrative only")


def _copy_overview(summary: OverviewSummary | None) -> OverviewPresentation | None:
    if summary is None:
        return None
    return OverviewPresentation(
        headline=summary.headline,
        summary=summary.summary,
        identity=summary.identity,
        balance=summary.balance,
        conclusion=summary.conclusion,
    )


def _copy_interpretation(
    narrative: InterpretationNarrative | None,
    consulting: ConsultingNarrative | None,
) -> InterpretationPresentation | None:
    if narrative is None:
        return None
    return InterpretationPresentation(
        overview=narrative.overview,
        observation=narrative.observation,
        reasoning=narrative.reasoning,
        meaning=narrative.meaning,
        impact=narrative.impact,
        recommendation=narrative.recommendation,
        closing=narrative.closing,
        consulting_flow=_optional_text(None if consulting is None else consulting.flow),
    )


def _copy_action(plan: ActionPlanNarrative | None) -> ActionPlanPresentation | None:
    if plan is None:
        return None
    top = None
    if plan.top_priority is not None:
        top = TopPriorityPresentation(
            title=plan.top_priority.title,
            description=plan.top_priority.description,
        )
    actions = tuple(
        ActionItemPresentation(
            title=item.title,
            description=item.description,
            category=item.category,
        )
        for item in plan.actions
    )
    warnings = tuple(
        WarningPresentation(title=item.title, description=item.description)
        for item in plan.warnings
    )
    period = None
    if plan.current_period is not None:
        period = CurrentPeriodPresentation(
            title=plan.current_period.title,
            description=plan.current_period.description,
        )
    return ActionPlanPresentation(
        top_priority=top,
        actions=actions,
        warnings=warnings,
        current_period=period,
    )


def _aggregate_status(
    summary: OverviewSummary | None,
    narrative: InterpretationNarrative | None,
    plan: ActionPlanNarrative | None,
    overview_view: OverviewPresentation | None,
    interpretation_view: InterpretationPresentation | None,
    action_view: ActionPlanPresentation | None,
) -> str:
    block_statuses = (
        _status_of(summary),
        _status_of(narrative),
        _status_of(plan),
    )
    if STATUS_INVALID in block_statuses:
        return STATUS_INVALID
    if not _has_usable_narrative(overview_view, interpretation_view, action_view):
        return STATUS_INSUFFICIENT
    required_complete = all(status == STATUS_COMPLETE for status in block_statuses)
    if required_complete:
        return STATUS_COMPLETE
    return STATUS_PARTIAL


def _status_of(block: object) -> str:
    if block is None:
        return STATUS_INSUFFICIENT
    status = getattr(block, "status", STATUS_INSUFFICIENT)
    if not isinstance(status, str):
        return STATUS_INSUFFICIENT
    return status


def _has_usable_narrative(
    overview: OverviewPresentation | None,
    interpretation: InterpretationPresentation | None,
    action_plan: ActionPlanPresentation | None,
) -> bool:
    if overview is not None and any(
        _has_text(value)
        for value in (overview.headline, overview.summary, overview.identity, overview.balance, overview.conclusion)
    ):
        return True
    if interpretation is not None and any(
        _has_text(value)
        for value in (
            interpretation.overview,
            interpretation.observation,
            interpretation.reasoning,
            interpretation.meaning,
            interpretation.impact,
            interpretation.recommendation,
            interpretation.closing,
            interpretation.consulting_flow,
        )
    ):
        return True
    if action_plan is None:
        return False
    if action_plan.top_priority is not None and (
        _has_text(action_plan.top_priority.title) or _has_text(action_plan.top_priority.description)
    ):
        return True
    return any(_has_text(item.title) or _has_text(item.description) for item in action_plan.actions)


def _has_text(value: str | None) -> bool:
    return bool(value and value.strip())


def _optional_text(value: str | None) -> str | None:
    if value is None or not value.strip():
        return None
    return value
