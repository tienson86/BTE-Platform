"""NarrativeV2Presentation — frozen public consumer contract."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.presentation.presentation_metadata import PresentationMetadata


@dataclass(frozen=True, slots=True)
class OverviewPresentation:
    """Public overview. Copied from OverviewSummary. No references."""

    headline: str | None
    summary: str | None
    identity: str | None
    balance: str | None
    conclusion: str | None


@dataclass(frozen=True, slots=True)
class InterpretationPresentation:
    """Public interpretation sections. Frozen contract fields only."""

    overview: str | None
    observation: str | None
    reasoning: str | None
    impact: str | None
    recommendation: str | None
    closing: str | None


@dataclass(frozen=True, slots=True)
class TopPriorityPresentation:
    """Public top priority. No decision_id."""

    title: str
    description: str


@dataclass(frozen=True, slots=True)
class ActionItemPresentation:
    """Public action. No knowledge or decision ids."""

    title: str
    description: str
    category: str


@dataclass(frozen=True, slots=True)
class WarningPresentation:
    """Public warning. No severity internals required by contract."""

    title: str
    description: str


@dataclass(frozen=True, slots=True)
class CurrentPeriodPresentation:
    """Public current period. Absent when upstream is None."""

    title: str
    description: str


@dataclass(frozen=True, slots=True)
class ActionPlanPresentation:
    """Public action plan. Copied from ActionPlanNarrative fields only."""

    top_priority: TopPriorityPresentation | None
    actions: tuple[ActionItemPresentation, ...]
    warnings: tuple[WarningPresentation, ...]
    current_period: CurrentPeriodPresentation | None


@dataclass(frozen=True, slots=True)
class NarrativeV2Presentation:
    """One immutable consumer contract. Not Dashboard/PDF/DOCX specific."""

    status: str
    overview: OverviewPresentation | None
    interpretation: InterpretationPresentation | None
    action_plan: ActionPlanPresentation | None
    commercial: None
    metadata: PresentationMetadata
