"""Relationship evidence models. Immutable factual atoms. No narrative."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceResolutionStatus,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)


@dataclass(frozen=True, slots=True)
class EvidenceSourceRef:
    """Trace from an evidence atom to Canonical source."""

    analysis_id: str
    person: PersonSide
    path: str
    value: Any = None


@dataclass(frozen=True, slots=True)
class MarriageEvidence:
    """One relationship evidence atom. Immutable after creation."""

    evidence_id: str
    domain: MarriageDomain
    evidence_type: MarriageEvidenceType
    direction: EvidenceDirection
    significance: EvidenceSignificance
    confidence: float
    subject: RelationshipSubject
    source_refs: tuple[EvidenceSourceRef, ...]
    rule_id: str | None = None
    description: str | None = None
    technical_payload: Mapping[str, Any] = field(default_factory=dict)
    predicate: str | None = None
    scope: str | None = None
    version: str | None = None
    policy_ref: str | None = None


@dataclass(frozen=True, slots=True)
class ResolvedMarriageEvidence:
    """Derived resolution overlay. Raw evidence remains unchanged."""

    evidence_id: str
    status: EvidenceResolutionStatus
    significance: EvidenceSignificance
    confidence: float
    conflicts_with: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    suppression_reason: str | None = None
    residual_impact: str | None = None
