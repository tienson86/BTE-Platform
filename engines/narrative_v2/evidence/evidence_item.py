"""EvidenceItem — smallest published fact unit."""

from __future__ import annotations

from dataclasses import dataclass

from engines.narrative_v2.evidence.evidence_reference import EvidenceReference

STATUS_AVAILABLE = "available"
STATUS_MISSING = "missing"
STATUS_UNSUPPORTED = "unsupported"
STATUS_INVALID = "invalid"

ALLOWED_STATUSES: frozenset[str] = frozenset(
    {
        STATUS_AVAILABLE,
        STATUS_MISSING,
        STATUS_UNSUPPORTED,
        STATUS_INVALID,
    }
)

EvidenceValue = str | int | float | bool | tuple[str | int | float | bool, ...] | None


@dataclass(frozen=True, slots=True)
class EvidenceItem:
    """One extracted canonical fact. No customer prose. No object dump."""

    evidence_id: str
    domain: str
    key: str
    label: str
    value: EvidenceValue
    source_path: str
    status: str
    references: tuple[EvidenceReference, ...]
    metadata: tuple[tuple[str, str], ...] = ()

    def to_trace_record(self) -> dict[str, object]:
        """Serialize a golden-trace row."""
        value: object = self.value
        if isinstance(value, tuple):
            value = list(value)
        return {
            "evidence_id": self.evidence_id,
            "domain": self.domain,
            "key": self.key,
            "value": value,
            "status": self.status,
            "source_path": self.source_path,
        }
