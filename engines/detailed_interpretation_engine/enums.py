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
    PARTIAL = "PARTIAL"
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


class ActivationState(str, Enum):
    """Luck-window expression state (DI-09). Not natal DomainState."""

    DORMANT = "dormant"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    PEAK = "peak"
    OVERLOADED = "overloaded"
    BLOCKED = "blocked"
    SUPPRESSED = "suppressed"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"


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


class TenGodPresenceState(str, Enum):
    """DI-01 presence, including overlays. Not importance."""

    ABSENT = "absent"
    HIDDEN_ONLY = "hidden_only"
    VISIBLE = "visible"
    VISIBLE_AND_ROOTED = "visible_and_rooted"
    REPEATED = "repeated"
    CONCENTRATED = "concentrated"
    STRUCTURALLY_DOMINANT = "structurally_dominant"
    UNRESOLVED = "unresolved"


class TenGodVisibilitySummary(str, Enum):
    """Summary visibility. Occurrences stay unflattened."""

    EXPOSED = "exposed"
    HIDDEN = "hidden"
    MIXED = "mixed"
    ABSENT = "absent"
    UNRESOLVED = "unresolved"


class TenGodRootState(str, Enum):
    """Root availability consumed from upstream hidden-stem facts."""

    NO_ROOT = "no_root"
    WEAK_ROOT = "weak_root"
    MODERATE_ROOT = "moderate_root"
    STRONG_ROOT = "strong_root"
    MULTIPLE_ROOTS = "multiple_roots"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class TenGodEffectiveStrength(str, Enum):
    """Local Ten God strength. Not Day Master Strength or Pattern Strength."""

    ABSENT = "absent"
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class TenGodStructuralRole(str, Enum):
    """Structural role consumed from upstream Pattern / capacity evidence."""

    PRIMARY_PATTERN = "primary_pattern"
    SECONDARY_PATTERN = "secondary_pattern"
    PATTERN_GENERATOR = "pattern_generator"
    PATTERN_SUPPORT = "pattern_support"
    PATTERN_CONTROLLER = "pattern_controller"
    DAMAGE_SOURCE = "damage_source"
    RESCUE_SOURCE = "rescue_source"
    CAPACITY_SUPPORT = "capacity_support"
    CAPACITY_PRESSURE = "capacity_pressure"
    NEUTRAL = "neutral"
    UNRESOLVED = "unresolved"


class TenGodUsability(str, Enum):
    """Contextual usability. Never good/bad."""

    SUPPORTIVE = "supportive"
    USABLE = "usable"
    CONDITIONALLY_USABLE = "conditionally_usable"
    NEUTRAL = "neutral"
    PRESSURING = "pressuring"
    CONFLICTING = "conflicting"
    DAMAGING = "damaging"
    RESCUED = "rescued"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class TenGodUsefulGodContext(str, Enum):
    """Useful God binding for one Ten God. Not inferred Dụng/Hỷ/Kỵ."""

    USEFUL = "useful"
    FAVORABLE = "favorable"
    UNFAVORABLE = "unfavorable"
    MIXED = "mixed"
    NEUTRAL = "neutral"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class DayMasterBand(str, Enum):
    """Consumed Strength Engine classification, collapsed for Ten God context."""

    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    UNRESOLVED = "unresolved"


class TenGodConfidenceBand(str, Enum):
    """Categorical confidence. No fake numeric precision."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    UNRESOLVED = "unresolved"


class CombinationState(str, Enum):
    """DI-02 combination state. Co-presence is not confirmed."""

    CONFIRMED = "confirmed"
    CONDITIONAL = "conditional"
    WEAK = "weak"
    INACTIVE = "inactive"
    BROKEN = "broken"
    UNRESOLVED = "unresolved"


class CombinationReach(str, Enum):
    """How a source reaches a target. Not a combination type."""

    DIRECT = "direct"
    INDIRECT = "indirect"
    MEDIATED = "mediated"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"


class CombinationRelativePower(str, Enum):
    """Relative power between source and target. Not a raw count."""

    SOURCE_DOMINANT = "source_dominant"
    TARGET_DOMINANT = "target_dominant"
    BALANCED = "balanced"
    MEDIATED = "mediated"
    UNCERTAIN = "uncertain"


class ChainQuality(str, Enum):
    """Chain quality is limited by the weakest meaningful link."""

    BROKEN = "broken"
    VERY_WEAK = "very_weak"
    WEAK = "weak"
    FUNCTIONAL = "functional"
    STRONG = "strong"
    VERY_STRONG = "very_strong"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"


class CombinationStructuralRole(str, Enum):
    """Importance of a combination. Not Pattern identity."""

    PRIMARY_STRUCTURAL_CHAIN = "primary_structural_chain"
    SECONDARY_STRUCTURAL_CHAIN = "secondary_structural_chain"
    SUPPORTING_CHAIN = "supporting_chain"
    DOMAIN_SPECIFIC_CHAIN = "domain_specific_chain"
    INCIDENTAL_RELATION = "incidental_relation"
    UNRESOLVED = "unresolved"


class EcosystemRole(str, Enum):
    """DI-04 ecosystem role. Not Ten God identity."""

    DRIVER = "driver"
    SUPPORTING = "supporting"
    SUPPRESSED = "suppressed"
    BLOCKED = "blocked"
    EXCESSIVE = "excessive"
    DEFICIENT = "deficient"
    MISSING = "missing"
    BOTTLENECK = "bottleneck"
    BALANCER = "balancer"
    NEUTRAL = "neutral"
    UNRESOLVED = "unresolved"


class FlowQuality(str, Enum):
    """Global flow quality. Cannot outrun the weakest meaningful link."""

    BROKEN = "broken"
    RESTRICTED = "restricted"
    CONDITIONAL = "conditional"
    FUNCTIONAL = "functional"
    STRONG = "strong"
    EXCELLENT = "excellent"
    UNRESOLVED = "unresolved"


class EcosystemState(str, Enum):
    """Whole-system balance. Not a second Grade."""

    HIGHLY_BALANCED = "highly_balanced"
    BALANCED = "balanced"
    SLIGHTLY_UNBALANCED = "slightly_unbalanced"
    MODERATELY_UNBALANCED = "moderately_unbalanced"
    HEAVILY_UNBALANCED = "heavily_unbalanced"
    FRAGMENTED = "fragmented"
    BLOCKED = "blocked"
    UNRESOLVED = "unresolved"


class ShenShaInterpretationState(str, Enum):
    """DI-05 per-star interpretation state. Not a life outcome."""

    APPLIED = "applied"
    BLOCKED_NO_DEPENDENCY = "blocked_no_dependency"
    DETECTED_NOT_MATERIAL = "detected_not_material"
    NOT_DETECTED = "not_detected"
    UNRESOLVED = "unresolved"


class ShenShaDependencyState(str, Enum):
    """Required structural dependency availability."""

    SATISFIED = "satisfied"
    PARTIAL = "partial"
    BLOCKED = "blocked"
    UNRESOLVED = "unresolved"
    NOT_AVAILABLE = "not_available"


class ShenShaModifierState(str, Enum):
    """How the star may modify interpretation confidence. Never good/bad."""

    APPLIED = "applied"
    WEAK_SUPPORT = "weak_support"
    QUALIFIED = "qualified"
    WARNING = "warning"
    BLOCKED = "blocked"
    INACTIVE = "inactive"
    UNRESOLVED = "unresolved"


class ShenShaConfidenceModifier(str, Enum):
    """Categorical confidence change. Does not change source classification."""

    STRENGTHEN = "strengthen"
    WEAKEN = "weaken"
    QUALIFY = "qualify"
    WARN = "warn"
    HIGHLIGHT = "highlight"
    NO_EFFECT = "no_effect"
    BLOCKED = "blocked"


class ShenShaClusterState(str, Enum):
    """DI-06 cluster state. Raw star count is not a state."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"


class ShenShaClusterStrength(str, Enum):
    """Cluster quality. Not a count of detected names."""

    NONE = "none"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"
    CONDITIONAL = "conditional"
    UNRESOLVED = "unresolved"
