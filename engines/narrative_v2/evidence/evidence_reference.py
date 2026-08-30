"""Evidence reference to a published CanonicalAnalysis path."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    """Traceability pointer. Not customer-facing."""

    source_path: str
    domain: str
