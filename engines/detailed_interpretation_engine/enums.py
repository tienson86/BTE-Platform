"""Pack 07 frozen enumerations.

Values are contract IDs. No scoring or inference lives here.
"""

from __future__ import annotations

from enum import Enum


class EvaluationStatus(str, Enum):
    """Stage evaluation status used across Pack 07 objects."""

    NOT_EVALUATED = "not_evaluated"
    RESOLVED = "resolved"
    PARTIALLY_RESOLVED = "partially_resolved"
    UNRESOLVED = "unresolved"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    NOT_APPLICABLE = "not_applicable"
    BLOCKED = "blocked"


class BindingState(str, Enum):
    """Implementation / binding state. Must not be conflated with EvaluationStatus."""

    NOT_IMPLEMENTED = "not_implemented"
    NOT_BOUND = "not_bound"
    NOT_EVALUATED = "not_evaluated"
    UNAVAILABLE = "unavailable"
    UNRESOLVED = "unresolved"
    EVALUATED = "evaluated"
    INVALID = "invalid"


class ValidationStatus(str, Enum):
    """Canonical validation outcome."""

    PASS = "PASS"
    PASS_WITH_WARNINGS = "PASS_WITH_WARNINGS"
    FAIL = "FAIL"


class IssueSeverity(str, Enum):
    """Validation issue severity."""

    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DiagnosticStatus(str, Enum):
    """Development-only Pack 07 runtime diagnostic status."""

    PASS = "PASS"
    READY = "READY"
    NOT_BOUND = "NOT_BOUND"
    NOT_EVALUATED = "NOT_EVALUATED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    WARNING = "WARNING"
    FAIL = "FAIL"


class TemporalLayer(str, Enum):
    """DI-11 temporal layers. natal is a parent context, not a layer."""

    LUCK_CYCLE = "luck_cycle"
    ANNUAL = "annual"
    MONTHLY = "monthly"
    DAILY = "daily"
    HOURLY = "hourly"


class DomainState(str, Enum):
    """Natal domain interpretive state (DI-08)."""

    VERY_STRONG = "very_strong"
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    CONDITIONAL = "conditional"
    BLOCKED = "blocked"
    FRAGMENTED = "fragmented"
    UNRESOLVED = "unresolved"
    NOT_EVALUATED = "not_evaluated"


class PriorityTier(str, Enum):
    """Evidence Priority tiers (DI-07)."""

    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


class NarrativeNodeType(str, Enum):
    """NarrativeGraph node types (DI-19)."""

    EXECUTIVE_SUMMARY = "executive_summary"
    STRENGTH = "strength"
    RISK = "risk"
    OPPORTUNITY = "opportunity"
    BOTTLENECK = "bottleneck"
    ACTION = "action"
    TEMPORAL = "temporal"
    SUPPORTING_EVIDENCE = "supporting_evidence"
    DOMAIN_SECTION = "domain_section"
    OPTIMIZATION_SECTION = "optimization_section"
    CLOSING_SUMMARY = "closing_summary"


class NarrativeEdgeType(str, Enum):
    """NarrativeGraph edge types (DI-19)."""

    SUPPORTS = "supports"
    EXPLAINS = "explains"
    QUALIFIES = "qualifies"
    CONTRASTS = "contrasts"
    EXPANDS = "expands"
    SUMMARIZES = "summarizes"


class NarrativeLayer(str, Enum):
    """Presentation density layers of one NarrativeGraph."""

    COMMERCIAL = "commercial"
    TECHNICAL = "technical"
    EXPERT = "expert"
    EXECUTIVE = "executive"


class ConsultingOperation(str, Enum):
    """Allowed or forbidden consulting operations (DI-20)."""

    RETRIEVE_BLOCK = "retrieve_block"
    RETRIEVE_TRACE = "retrieve_trace"
    RETRIEVE_EVIDENCE = "retrieve_evidence"
    RETRIEVE_OPTIMIZATION_ACTION = "retrieve_optimization_action"
    RECOMPUTE_PATTERN = "recompute_pattern"
    RERANK_EVIDENCE = "rerank_evidence"
    INVENT_ACTION = "invent_action"
    MUTATE_CONTRACT = "mutate_contract"


class HourCompleteness(str, Enum):
    """Chart hour completeness consumed from identity, not inferred."""

    COMPLETE = "complete"
    MISSING = "missing"
    UNKNOWN = "unknown"
