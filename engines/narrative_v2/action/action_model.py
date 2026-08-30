"""ActionPlanNarrative and related customer-facing action units."""

from __future__ import annotations

from dataclasses import dataclass

STATUS_COMPLETE = "complete"
STATUS_PARTIAL = "partial"
STATUS_INSUFFICIENT = "insufficient"
STATUS_INVALID = "invalid"

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_COMPLETE,
        STATUS_PARTIAL,
        STATUS_INSUFFICIENT,
        STATUS_INVALID,
    }
)

MAX_ACTIONS = 6
MIN_ACTIONS_FOR_COMPLETE = 3

ACTION_VERSION = "nimp08.1.0"


@dataclass(frozen=True, slots=True)
class ActionReference:
    """Provenance for one Action Plan field."""

    field: str
    rewrite_ids: tuple[str, ...]
    knowledge_ids: tuple[str, ...]
    reasoning_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    decision_ids: tuple[str, ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        return {
            "field": self.field,
            "rewrite_ids": list(self.rewrite_ids),
            "knowledge_ids": list(self.knowledge_ids),
            "reasoning_ids": list(self.reasoning_ids),
            "evidence_ids": list(self.evidence_ids),
            "decision_ids": list(self.decision_ids),
        }


@dataclass(frozen=True, slots=True)
class TopPriority:
    """Exactly one customer-facing priority when a Decision exists."""

    title: str
    description: str
    decision_id: str


@dataclass(frozen=True, slots=True)
class ActionItem:
    """One concrete customer action. Must reference a Decision."""

    action_id: str
    decision_id: str
    title: str
    description: str
    category: str
    priority: int
    source_knowledge_ids: tuple[str, ...]
    references: tuple[ActionReference, ...]
    status: str
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        return {
            "action_id": self.action_id,
            "decision_id": self.decision_id,
            "title": self.title,
            "category": self.category,
            "priority": self.priority,
            "source_knowledge_ids": list(self.source_knowledge_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class WarningItem:
    """Approved caution. Not fear. Not prediction."""

    warning_id: str
    title: str
    description: str
    severity: str
    source_knowledge_ids: tuple[str, ...]
    references: tuple[ActionReference, ...]
    status: str
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        return {
            "warning_id": self.warning_id,
            "title": self.title,
            "severity": self.severity,
            "source_knowledge_ids": list(self.source_knowledge_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class CurrentPeriod:
    """Approved current-period guidance. Not a luck-name inference."""

    title: str
    description: str
    source_knowledge_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ActionPlanNarrative:
    """Customer action plan. Not Interpretation. Not Presentation."""

    top_priority: TopPriority | None
    actions: tuple[ActionItem, ...]
    warnings: tuple[WarningItem, ...]
    current_period: CurrentPeriod | None
    references: tuple[ActionReference, ...]
    metadata: tuple[tuple[str, str], ...]
    status: str

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No unrelated payload."""
        rows: list[dict[str, object]] = []
        for action in self.actions:
            rows.append(action.to_trace_record())
        for warning in self.warnings:
            rows.append(warning.to_trace_record())
        rows.extend(entry.to_trace_record() for entry in self.references)
        return rows
