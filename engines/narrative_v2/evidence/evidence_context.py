"""NarrativeEvidenceContext — extracted canonical facts only."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.evidence.evidence_item import EvidenceItem
from engines.narrative_v2.evidence.evidence_reference import EvidenceReference


@dataclass(frozen=True, slots=True)
class EvidenceContractGap:
    """Requested evidence field not published by CanonicalAnalysis."""

    field: str
    reason: str
    source_path: str | None = None


@dataclass(frozen=True, slots=True)
class NarrativeEvidenceContext:
    """Evidence context. No meaning, reasoning, or recommendation."""

    identity: tuple[EvidenceItem, ...]
    calendar: tuple[EvidenceItem, ...]
    bazi: tuple[EvidenceItem, ...]
    strength: tuple[EvidenceItem, ...]
    temperature: tuple[EvidenceItem, ...]
    pattern: tuple[EvidenceItem, ...]
    useful_god: tuple[EvidenceItem, ...]
    five_elements: tuple[EvidenceItem, ...]
    ten_gods: tuple[EvidenceItem, ...]
    shensha: tuple[EvidenceItem, ...]
    luck: tuple[EvidenceItem, ...]
    references: tuple[EvidenceReference, ...]
    metadata: tuple[tuple[str, str], ...]
    items: tuple[EvidenceItem, ...]
    contract_gaps: tuple[EvidenceContractGap, ...]

    def item(self, evidence_id: str) -> EvidenceItem | None:
        """Return one item by deterministic id."""
        for entry in self.items:
            if entry.evidence_id == evidence_id:
                return entry
        return None

    def to_trace_records(self) -> list[dict[str, object]]:
        """Golden-trace rows. No customer prose. No debug dump."""
        return [item.to_trace_record() for item in self.items]
