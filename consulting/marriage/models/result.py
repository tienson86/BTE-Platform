"""Canonical factual marriage decision result."""

from __future__ import annotations

from dataclasses import dataclass

from consulting.marriage.models.confidence import MarriageConfidenceResult
from consulting.marriage.models.decision import MarriageDomainResults, MarriageOverallDecision
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.person import MarriagePersonReference
from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.models.timing import MarriageTimingResult
from consulting.marriage.models.versioning import MarriageVersionBundle


@dataclass(slots=True)
class MarriageDecisionResult:
    """Factual canonical output of TV-01. Not a presentation payload."""

    consultation_id: str
    person_a: MarriagePersonReference
    person_b: MarriagePersonReference
    canonical_a: MarriageCanonicalSnapshot
    canonical_b: MarriageCanonicalSnapshot
    evidence: list[MarriageEvidence]
    domains: MarriageDomainResults
    overall: MarriageOverallDecision
    recommendations: list[MarriageRecommendation]
    confidence: MarriageConfidenceResult
    versions: MarriageVersionBundle
    created_at: str
    timing: MarriageTimingResult | None = None
