"""Relationship evidence models. Immutable factual atoms. No narrative."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)


@dataclass(slots=True)
class EvidenceSourceRef:
    """Trace from an evidence atom to Canonical source."""

    analysis_id: str
    person: PersonSide
    path: str
    value: Any = None


@dataclass(slots=True)
class MarriageEvidence:
    """One relationship evidence atom."""

    evidence_id: str
    domain: MarriageDomain
    evidence_type: MarriageEvidenceType
    direction: EvidenceDirection
    significance: EvidenceSignificance
    confidence: float
    subject: RelationshipSubject
    source_refs: list[EvidenceSourceRef]
    rule_id: str | None = None
    description: str | None = None
    technical_payload: dict[str, Any] = field(default_factory=dict)
