"""Canonical runtime adapter contract. Read-only. No Canonical writes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Mapping

from consulting.marriage.dto.request import MarriagePersonInput
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot

CanonicalAnalysis = Mapping[str, Any]


class CanonicalRuntimeAdapter(ABC):
    """Adapter to Canonical Runtime. TV-01 must not modify Canonical Truth."""

    @abstractmethod
    def analyze(self, birth_input: MarriagePersonInput) -> CanonicalAnalysis:
        """Run Canonical analysis for one person."""

    @abstractmethod
    def to_snapshot(self, analysis: CanonicalAnalysis) -> MarriageCanonicalSnapshot:
        """Select and bind a marriage snapshot from Canonical analysis."""
