"""MC-01 frozen enumerations as string constants used by models."""

from __future__ import annotations

from enum import Enum


class MingJuDecisionStatus(str, Enum):
    """Root result status."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    UNRESOLVED = "unresolved"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    INVALID_INPUT = "invalid_input"


class AnalysisState(str, Enum):
    """Reusable analysis state."""

    RESOLVED = "resolved"
    PARTIALLY_RESOLVED = "partially_resolved"
    UNRESOLVED = "unresolved"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    NOT_APPLICABLE = "not_applicable"


class IntegrityState(str, Enum):
    """Structural integrity classification."""

    COMPLETE = "complete"
    SUBSTANTIALLY_COMPLETE = "substantially_complete"
    CONDITIONALLY_COMPLETE = "conditionally_complete"
    MIXED = "mixed"
    DAMAGED_BUT_RESCUED = "damaged_but_rescued"
    DAMAGED = "damaged"
    FAILED = "failed"
    UNRESOLVED = "unresolved"


class PatternGrade(str, Enum):
    """MC-01 structural Pattern Grade. Not ScoreEngine customer grade."""

    SS = "SS"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    UNRESOLVED = "UNRESOLVED"
