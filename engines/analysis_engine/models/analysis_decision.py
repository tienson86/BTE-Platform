"""Analysis decision model."""

from __future__ import annotations

from dataclasses import dataclass

from engines.analysis_engine.models.analysis_evidence import AnalysisEvidence
from engines.analysis_engine.models.analysis_metadata import AnalysisMetadata, ModelTimestamps


@dataclass(frozen=True, slots=True)
class AnalysisDecision:
    """Immutable decision contract produced by analysis stages."""

    id: str
    version: str
    metadata: AnalysisMetadata
    trace: tuple[str, ...]
    timestamps: ModelTimestamps
    decision_type: str
    outcome: str
    confidence: float | None = None
    evidence: tuple[AnalysisEvidence, ...] = ()

    def validate(self) -> bool:
        """Validate analysis decision contract."""
        raise NotImplementedError
