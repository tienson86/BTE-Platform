"""Domain interpretation contracts for generic composition."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DomainStatus(str, Enum):
    """Domain composition status."""

    AVAILABLE = "AVAILABLE"
    PARTIAL = "PARTIAL"
    NOT_AVAILABLE = "NOT_AVAILABLE"
    INSUFFICIENT = "INSUFFICIENT"


class KnowledgeStatus(str, Enum):
    """Knowledge readiness for validation diagnostics only."""

    FROZEN = "FROZEN"
    DRAFT_KNOWLEDGE = "DRAFT_KNOWLEDGE"
    PILOT = "PILOT"
    MISSING = "MISSING"


class ConflictClass(str, Enum):
    """Cross-domain conflict classification."""

    TRUE_CONFLICT = "TRUE_CONFLICT"
    CONDITIONAL_NUANCE = "CONDITIONAL_NUANCE"
    DIFFERENT_SCOPE = "DIFFERENT_SCOPE"


@dataclass(slots=True)
class DomainSection:
    """One customer-facing interpretation section."""

    section_id: str
    title: str
    paragraphs: list[str] = field(default_factory=list)
    theme_ids: list[str] = field(default_factory=list)

    def to_customer_dict(self) -> dict[str, Any]:
        """Customer serialization — hide theme internals."""
        return {
            "section_id": self.section_id,
            "title": self.title,
            "body": "\n\n".join(self.paragraphs),
        }


@dataclass(slots=True)
class DomainClaim:
    """Traceable claim for integration — not customer-visible."""

    claim_id: str
    theme_id: str
    text: str
    domain: str
    polarity: str = "neutral"


@dataclass(slots=True)
class DomainInterpretationResult:
    """Generic domain interpretation result."""

    domain: str
    status: DomainStatus
    conclusion: str = ""
    sections: list[DomainSection] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    executive_claims: list[str] = field(default_factory=list)
    missing_data: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    version: str = "1.0.0"
    knowledge_status: KnowledgeStatus = KnowledgeStatus.PILOT
    claims: list[DomainClaim] = field(default_factory=list)

    def to_customer_dict(self) -> dict[str, Any]:
        """Customer serialization — hide diagnostics and claim traces."""
        return {
            "domain": self.domain,
            "status": self.status.value,
            "conclusion": self.conclusion,
            "sections": [section.to_customer_dict() for section in self.sections],
            "recommendations": list(self.recommendations),
            "executive_claims": list(self.executive_claims),
            "missing_data": list(self.missing_data),
            "version": self.version,
        }

    def to_validation_dict(self) -> dict[str, Any]:
        """Validation serialization — retain diagnostics."""
        payload = self.to_customer_dict()
        payload["knowledge_status"] = self.knowledge_status.value
        payload["diagnostics"] = dict(self.diagnostics)
        payload["claims"] = [
            {
                "claim_id": claim.claim_id,
                "theme_id": claim.theme_id,
                "text": claim.text,
                "domain": claim.domain,
                "polarity": claim.polarity,
            }
            for claim in self.claims
        ]
        return payload


@dataclass(slots=True)
class CrossDomainConflict:
    """Detected cross-domain conflict."""

    conflict_id: str
    classification: ConflictClass
    domain_a: str
    domain_b: str
    claim_a: str
    claim_b: str
    resolution: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize conflict for diagnostics."""
        return {
            "conflict_id": self.conflict_id,
            "classification": self.classification.value,
            "domain_a": self.domain_a,
            "domain_b": self.domain_b,
            "claim_a": self.claim_a,
            "claim_b": self.claim_b,
            "resolution": self.resolution,
        }


@dataclass(slots=True)
class IntegratedInterpretationContext:
    """Cross-domain integration context — not raw prose concatenation."""

    claims: list[DomainClaim] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    missing_domains: list[str] = field(default_factory=list)
    conflicts: list[CrossDomainConflict] = field(default_factory=list)
    suppressed_duplicates: list[str] = field(default_factory=list)
    domain_results: dict[str, DomainInterpretationResult] = field(default_factory=dict)

    def to_diagnostics_dict(self) -> dict[str, Any]:
        """Validation diagnostics for integrated context."""
        return {
            "themes": list(self.themes),
            "recommendations": list(self.recommendations),
            "warnings": list(self.warnings),
            "missing_domains": list(self.missing_domains),
            "conflicts": [item.to_dict() for item in self.conflicts],
            "suppressed_duplicates": list(self.suppressed_duplicates),
            "claim_count": len(self.claims),
        }


@dataclass(slots=True)
class ExecutiveConsultingResult:
    """Generic executive consulting composition result."""

    status: DomainStatus
    body: str
    sections: list[DomainSection] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    knowledge_status: KnowledgeStatus = KnowledgeStatus.PILOT
    diagnostics: dict[str, Any] = field(default_factory=dict)

    def to_customer_dict(self) -> dict[str, Any]:
        """Customer serialization."""
        return {
            "status": self.status.value,
            "body": self.body,
            "sections": [section.to_customer_dict() for section in self.sections],
            "recommendations": list(self.recommendations),
            "version": self.version,
        }
