"""Canonical adapter placeholder. No Canonical engine calls in TV1-B01."""

from __future__ import annotations

from consulting.marriage.adapters.contract import CanonicalAnalysis, CanonicalRuntimeAdapter
from consulting.marriage.dto.request import MarriagePersonInput
from consulting.marriage.models.snapshot import MarriageCanonicalSnapshot


class PlaceholderCanonicalRuntimeAdapter(CanonicalRuntimeAdapter):
    """Skeleton placeholder. Does not invoke Calendar, BaZi, or other Canonical engines."""

    def analyze(self, birth_input: MarriagePersonInput) -> CanonicalAnalysis:
        """Refuse Canonical analysis. Runtime integration belongs to TV1-B02."""
        raise NotImplementedError("TV1-B01: Canonical adapter is not implemented")

    def to_snapshot(self, analysis: CanonicalAnalysis) -> MarriageCanonicalSnapshot:
        """Refuse snapshot mapping. Runtime integration belongs to TV1-B02."""
        raise NotImplementedError("TV1-B01: Canonical snapshot mapping is not implemented")
