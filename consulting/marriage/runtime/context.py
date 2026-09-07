"""Marriage runtime context. Internal orchestration object. Not a public API."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from consulting.marriage.dto.request import NormalizedMarriageRequest
from consulting.marriage.dto.response import RuntimeWarning, StageTiming
from consulting.marriage.models.confidence import MarriageConfidenceResult
from consulting.marriage.models.decision import MarriageDomainResults, MarriageOverallDecision
from consulting.marriage.models.evidence import MarriageEvidence, ResolvedMarriageEvidence
from consulting.marriage.models.finding import MarriageFinding
from consulting.marriage.models.recommendation import MarriageRecommendation
from consulting.marriage.models.result import MarriageDecisionResult
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot
from consulting.marriage.models.timing import MarriageTimingResult
from consulting.marriage.models.versioning import MarriageVersionBundle

CanonicalAnalysis = Mapping[str, Any]


@dataclass(slots=True)
class MarriageRuntimeContext:
    """Per-consultation runtime state. No global mutable state."""

    consultation_id: str
    request: NormalizedMarriageRequest
    versions: MarriageVersionBundle
    analysis_a: CanonicalAnalysis | None = None
    analysis_b: CanonicalAnalysis | None = None
    snapshot_a: MarriageCanonicalSnapshot | None = None
    snapshot_b: MarriageCanonicalSnapshot | None = None
    evidence: list[MarriageEvidence] | None = None
    resolved_evidence: list[ResolvedMarriageEvidence] | None = None
    findings: list[MarriageFinding] | None = None
    domain_results: MarriageDomainResults | None = None
    overall: MarriageOverallDecision | None = None
    decision_result: MarriageDecisionResult | None = None
    timing: MarriageTimingResult | None = None
    recommendations: list[MarriageRecommendation] | None = None
    confidence: MarriageConfidenceResult | None = None
    warnings: list[RuntimeWarning] = field(default_factory=list)
    timings: list[StageTiming] = field(default_factory=list)
