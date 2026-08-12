"""Cross-Domain Reasoning Engine V1.1 — contracts and enums."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuestionContext(str, Enum):
    """Feature query context — affects salience, not factual truth."""

    GENERAL = "GENERAL"
    IDENTITY = "IDENTITY"
    CAREER = "CAREER"


class ClaimScope(str, Enum):
    """Scope of a domain claim — conflicts require overlapping scopes."""

    BODY_STRENGTH = "BODY_STRENGTH"
    STRUCTURAL_PATTERN = "STRUCTURAL_PATTERN"
    OPERATING_STYLE = "OPERATING_STYLE"
    BALANCE_STRATEGY = "BALANCE_STRATEGY"
    CAREER = "CAREER"
    RELATIONSHIP = "RELATIONSHIP"
    GENERAL = "GENERAL"


class ClaimType(str, Enum):
    """Normalized claim categories."""

    CLASSIFICATION = "CLASSIFICATION"
    OPERATING_ROLE = "OPERATING_ROLE"
    STRUCTURE = "STRUCTURE"
    BALANCE = "BALANCE"
    RECOMMENDATION = "RECOMMENDATION"
    CONSTRAINT = "CONSTRAINT"
    SUPPORT = "SUPPORT"


class RelationType(str, Enum):
    """Frozen cross-domain relation types."""

    AGREEMENT = "AGREEMENT"
    REINFORCEMENT = "REINFORCEMENT"
    CONDITIONAL_NUANCE = "CONDITIONAL_NUANCE"
    DIFFERENT_SCOPE = "DIFFERENT_SCOPE"
    DEPENDENCY_OVERRIDE = "DEPENDENCY_OVERRIDE"
    TRUE_CONFLICT = "TRUE_CONFLICT"
    UNRESOLVED = "UNRESOLVED"
    NOT_COMPARABLE = "NOT_COMPARABLE"


class ThemeStatus(str, Enum):
    """Theme selection status."""

    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    SUPPORTING = "SUPPORTING"
    SUPPRESSED = "SUPPRESSED"
    UNRESOLVED = "UNRESOLVED"


class ConfidenceState(str, Enum):
    """Claim/theme confidence."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    UNRESOLVED = "UNRESOLVED"


@dataclass(slots=True)
class DomainClaim:
    """Normalized domain conclusion for cross-domain reasoning."""

    claim_id: str
    domain: str
    claim_type: ClaimType
    subject: str
    value: str
    scope: ClaimScope
    strength: float = 1.0
    dependencies: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    confidence_state: ConfidenceState = ConfidenceState.MEDIUM
    customer_relevance: float = 0.5
    question_relevance: float = 0.5
    version: str = "1.0.0"
    raw_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Validation serialization."""
        return {
            "claim_id": self.claim_id,
            "domain": self.domain,
            "claim_type": self.claim_type.value,
            "subject": self.subject,
            "value": self.value,
            "scope": self.scope.value,
            "strength": self.strength,
            "dependencies": list(self.dependencies),
            "evidence_refs": list(self.evidence_refs),
            "confidence_state": self.confidence_state.value,
            "customer_relevance": self.customer_relevance,
            "question_relevance": self.question_relevance,
            "version": self.version,
            "raw_text": self.raw_text,
        }


@dataclass(slots=True)
class CrossDomainRelation:
    """Relation between two claims."""

    relation_id: str
    relation_type: RelationType
    claim_a_id: str
    claim_b_id: str
    rationale: str
    policy_ref: str = ""
    customer_safe_state: str = ""
    unresolved_blocker: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Validation serialization."""
        return {
            "relation_id": self.relation_id,
            "relation_type": self.relation_type.value,
            "claim_a_id": self.claim_a_id,
            "claim_b_id": self.claim_b_id,
            "rationale": self.rationale,
            "policy_ref": self.policy_ref,
            "customer_safe_state": self.customer_safe_state,
            "unresolved_blocker": self.unresolved_blocker,
        }


@dataclass(slots=True)
class ReasoningTheme:
    """Chart-specific theme derived from supporting claims."""

    theme_id: str
    label: str
    supporting_claims: list[str] = field(default_factory=list)
    opposing_claims: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    salience: float = 0.0
    confidence_state: ConfidenceState = ConfidenceState.MEDIUM
    customer_value: float = 0.5
    status: ThemeStatus = ThemeStatus.SUPPORTING

    def to_dict(self) -> dict[str, Any]:
        """Validation serialization."""
        return {
            "theme_id": self.theme_id,
            "label": self.label,
            "supporting_claims": list(self.supporting_claims),
            "opposing_claims": list(self.opposing_claims),
            "domains": list(self.domains),
            "salience": self.salience,
            "confidence_state": self.confidence_state.value,
            "customer_value": self.customer_value,
            "status": self.status.value,
        }


@dataclass(slots=True)
class ExecutiveClaimPlan:
    """Non-prose executive slots for composers."""

    identity_core: str = ""
    operating_style: str = ""
    main_support: str = ""
    main_constraint: str = ""
    balance_direction: str = ""
    primary_insight: str = ""
    priorities: list[str] = field(default_factory=list)
    avoidances: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize claim plan."""
        return {
            "identity_core": self.identity_core,
            "operating_style": self.operating_style,
            "main_support": self.main_support,
            "main_constraint": self.main_constraint,
            "balance_direction": self.balance_direction,
            "primary_insight": self.primary_insight,
            "priorities": list(self.priorities),
            "avoidances": list(self.avoidances),
            "unresolved": list(self.unresolved),
        }


@dataclass(slots=True)
class CrossDomainReasoningInput:
    """Canonical input to the cross-domain reasoner."""

    strength_level: str = ""
    strength_score: float = 0.0
    pattern_key: str = ""
    pattern_label: str = ""
    pattern_than_vuong_nhuoc: str = ""
    tong_cach: str = ""
    ten_gods_primary: list[str] = field(default_factory=list)
    ten_gods_secondary: list[str] = field(default_factory=list)
    ten_gods_families: list[str] = field(default_factory=list)
    useful_god: str = ""
    useful_reasoning: str = ""
    favorable: list[str] = field(default_factory=list)
    unfavorable: list[str] = field(default_factory=list)
    domain_conclusions: dict[str, str] = field(default_factory=dict)
    missing_domains: list[str] = field(default_factory=list)
    question_context: QuestionContext = QuestionContext.GENERAL
    versions: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class CrossDomainReasoningResult:
    """Deterministic cross-domain reasoning output — no final prose."""

    claims: list[DomainClaim] = field(default_factory=list)
    relations: list[CrossDomainRelation] = field(default_factory=list)
    agreements: list[str] = field(default_factory=list)
    tensions: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)
    themes: list[ReasoningTheme] = field(default_factory=list)
    primary_theme: str = ""
    executive_claim_plan: ExecutiveClaimPlan = field(default_factory=ExecutiveClaimPlan)
    question_context: QuestionContext = QuestionContext.GENERAL
    customer_safe_conclusions: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    versions: dict[str, str] = field(default_factory=dict)

    def to_validation_dict(self) -> dict[str, Any]:
        """Full validation serialization."""
        return {
            "claims": [c.to_dict() for c in self.claims],
            "relations": [r.to_dict() for r in self.relations],
            "agreements": list(self.agreements),
            "tensions": list(self.tensions),
            "conflicts": list(self.conflicts),
            "unresolved": list(self.unresolved),
            "themes": [t.to_dict() for t in self.themes],
            "primary_theme": self.primary_theme,
            "executive_claim_plan": self.executive_claim_plan.to_dict(),
            "question_context": self.question_context.value,
            "customer_safe_conclusions": list(self.customer_safe_conclusions),
            "diagnostics": dict(self.diagnostics),
            "versions": dict(self.versions),
        }

    def to_customer_safe_dict(self) -> dict[str, Any]:
        """Customer-visible conclusions only — no enums/IDs."""
        return {
            "conclusions": list(self.customer_safe_conclusions),
            "primary_theme_label": next(
                (t.label for t in self.themes if t.theme_id == self.primary_theme),
                "",
            ),
            "unresolved_notes": [
                c
                for c in self.customer_safe_conclusions
                if c.startswith("Dữ liệu") or "hai khía cạnh" in c.lower() or "điều kiện" in c.lower()
            ],
        }
