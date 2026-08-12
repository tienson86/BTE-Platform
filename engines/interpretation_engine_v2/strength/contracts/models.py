"""Frozen contract models for Strength Interpretation Runtime V2."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AudienceMode(str, Enum):
    """Output audience mode."""

    CUSTOMER = "customer"
    VALIDATION = "validation"


class LanguageStrength(str, Enum):
    """Frozen language strength enum."""

    FIRM = "firm"
    QUALIFIED = "qualified"
    CAUTIOUS = "cautious"


class EvidenceState(str, Enum):
    """Frozen evidence states."""

    AVAILABLE = "AVAILABLE"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"
    MISSING = "MISSING"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    INACTIVE = "INACTIVE"


class GateState(str, Enum):
    """Evidence gate outcome."""

    ELIGIBLE = "eligible"
    PARTIALLY_SUPPORTED = "partially_supported"
    INELIGIBLE = "ineligible"


@dataclass(slots=True)
class FactRecord:
    """Normalized published fact."""

    fact_id: str
    dimension: str
    state: EvidenceState
    polarity: str = "neutral"
    observed: str = ""
    evidence_ids: list[str] = field(default_factory=list)


@dataclass(slots=True)
class KnowledgeUnit:
    """One catalog Knowledge Unit."""

    knowledge_id: str
    title: str
    pack: str
    topic: str
    purpose: str
    domain: str
    strength_class: str
    customer_mode: str
    validation_mode: str
    required_facts: list[str]
    optional_facts: list[str]
    forbidden_conditions: list[str]
    required_evidence: str
    customer_value: str
    specificity: str
    priority: str
    duplicate_cluster: str
    conflicts_with: list[str]
    reason_codes: list[str]
    narrative_weight: str
    version: str
    status: str
    source_document: str
    claim: str
    supporting_points: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PublishedStrengthFacts:
    """Published Strength facts for PACK-01 runtime."""

    case_id: str
    class_id: str
    strength_score: float
    facts: dict[str, EvidenceState]
    polarities: dict[str, str] = field(default_factory=dict)
    forbidden_flags: dict[str, bool] = field(default_factory=dict)
    interpretation_confidence: int = 72
    confidence_band: str = "high"
    alternative_primary: str = "strong"
    alternative_runner_up: str = "balanced"
    alternative_shares: dict[str, float] = field(default_factory=dict)
    conflicts: list[str] = field(default_factory=list)
    locale: str = "vi"


@dataclass(slots=True)
class ReasoningInput:
    """Reasoning engine input contract."""

    published: PublishedStrengthFacts
    candidates: list[KnowledgeUnit] = field(default_factory=list)
    audience: AudienceMode = AudienceMode.CUSTOMER
    knowledge_version: str = "1.0.0"
    reasoning_policy_version: str = "1.0.0"


@dataclass(slots=True)
class GateResult:
    """Per-unit evidence gate result."""

    knowledge_id: str
    state: GateState
    reason_code: str
    missing_required: list[str] = field(default_factory=list)
    forbidden_hit: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SelectedUnit:
    """Unit selected into the narrative plan."""

    knowledge_id: str
    reason_code: str
    merged_with: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RejectedUnit:
    """Unit rejected from the narrative plan."""

    knowledge_id: str
    reason_code: str


@dataclass(slots=True)
class SectionPlan:
    """One narrative section in the plan."""

    section_id: str
    purpose: str
    intent: str
    selected_units: list[SelectedUnit] = field(default_factory=list)
    rejected_units: list[RejectedUnit] = field(default_factory=list)
    language_strength: LanguageStrength = LanguageStrength.FIRM
    insufficient_data: bool = False
    insufficient_reason: str = ""
    transition_requirement: str = ""


@dataclass(slots=True)
class ClaimTrace:
    """Audit trace for one claim."""

    claim_id: str
    customer_section: str
    knowledge_ids: list[str]
    reason_codes: list[str]
    fact_ids: list[str]
    gate_state: str
    language_strength: LanguageStrength
    mode: AudienceMode


@dataclass(slots=True)
class NarrativePlan:
    """Primary reasoning output — no customer sentences."""

    meta: dict[str, str]
    primary_conclusion: dict[str, Any]
    sections: list[SectionPlan]
    warnings: list[str] = field(default_factory=list)
    omitted_domains: list[str] = field(default_factory=list)
    missing_data: list[str] = field(default_factory=list)
    alternative: dict[str, Any] = field(default_factory=dict)
    executive_summary_plan: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ComposedSection:
    """One composed section with prose."""

    section_id: str
    title: str
    paragraphs: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InterpretationMeta:
    """Result metadata."""

    case_id: str
    catalog_version: str
    reasoning_policy_version: str
    knowledge_version: str


@dataclass(slots=True)
class InterpretationResult:
    """Final runtime output for one audience mode bundle."""

    meta: InterpretationMeta
    narrative_plan: NarrativePlan
    validation_mode: list[ComposedSection]
    customer_mode: list[ComposedSection]
    diagnostics: dict[str, Any] = field(default_factory=dict)


class StrengthInterpretationError(Exception):
    """Base error for Strength interpretation runtime."""


class InvalidInputError(StrengthInterpretationError):
    """Input failed validation."""


class CatalogLoadError(StrengthInterpretationError):
    """Catalog could not be loaded."""
