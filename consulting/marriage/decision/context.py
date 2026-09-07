"""Marriage decision context. Input to Decision. No resolution logic."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.finding import MarriageFinding
from consulting.marriage.models.versioning import MarriageVersionBundle


@dataclass(slots=True)
class MarriageDecisionContext:
    """Decision-layer context. Evidence and findings are inputs, not conclusions here."""

    consultation_id: str
    relationship: MarriageRelationshipContext
    versions: MarriageVersionBundle
    evidence: list[MarriageEvidence] = field(default_factory=list)
    findings: list[MarriageFinding] = field(default_factory=list)
