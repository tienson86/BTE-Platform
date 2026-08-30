"""Golden Dataset registry. Append-only version index."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

STATUS_FROZEN = "FROZEN"


@dataclass(frozen=True, slots=True)
class GoldenRegistryEntry:
    """One immutable registry row for a Golden Case version."""

    case_id: str
    version: int
    status: str
    created: str
    reviewer: str

    def to_record(self) -> dict[str, Any]:
        """Serialize a registry row."""
        return {
            "case_id": self.case_id,
            "version": self.version,
            "status": self.status,
            "created": self.created,
            "reviewer": self.reviewer,
        }

    @classmethod
    def from_record(cls, payload: Mapping[str, Any]) -> GoldenRegistryEntry:
        """Rehydrate a registry row."""
        return cls(
            case_id=str(payload.get("case_id") or ""),
            version=int(payload.get("version") or 0),
            status=str(payload.get("status") or STATUS_FROZEN),
            created=str(payload.get("created") or ""),
            reviewer=str(payload.get("reviewer") or ""),
        )


def latest_version(rows: list[GoldenRegistryEntry], case_id: str) -> int:
    """Return the highest frozen version for a case, or 0 when absent."""
    versions = [row.version for row in rows if row.case_id == case_id]
    return max(versions) if versions else 0
