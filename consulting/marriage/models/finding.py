"""Finding models. Derived from evidence. Not customer prose."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import (
    EvidenceDirection,
    FindingPriority,
    FindingRelation,
    FindingType,
    MarriageDomain,
)


@dataclass(slots=True)
class FindingReference:
    """Cross-domain reference between findings."""

    finding_id: str
    relation: FindingRelation


@dataclass(slots=True)
class MarriageFinding:
    """One semantic finding derived from evidence."""

    finding_id: str
    domain: MarriageDomain
    type: FindingType
    priority: FindingPriority
    direction: EvidenceDirection
    confidence: float
    evidence_ids: list[str]
    title_key: str | None = None
    summary_key: str | None = None
    recommendation_ids: list[str] = field(default_factory=list)
    technical_summary: str | None = None
    semantic_key: str | None = None
    conflicting_evidence_ids: list[str] = field(default_factory=list)
    conditions: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    version: str | None = None
