"""Confidence models. Independent of compatibility score."""

from __future__ import annotations

from dataclasses import dataclass, field

from consulting.marriage.models.enums import ConfidenceLevel


@dataclass(slots=True)
class MarriageConfidenceResult:
    """Confidence of a marriage decision. Not a compatibility score."""

    overall: float
    data_quality: float
    evidence_quality: float
    engine_coverage: float
    level: ConfidenceLevel
    conflicts_penalty: float | None = None
    limitations: list[str] = field(default_factory=list)
