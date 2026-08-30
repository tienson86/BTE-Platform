"""Immutable Golden Case. Certified Presentation baseline only."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from engines.narrative_v2.golden.golden_serializer import freeze_mapping, thaw_mapping

GOLDEN_SCHEMA_VERSION = "bte.golden.v1"
STATUS_FROZEN = "FROZEN"


@dataclass(frozen=True, slots=True)
class GoldenCase:
    """One frozen certified baseline. Never mutated after promotion."""

    case_id: str
    presentation: Mapping[str, Any]
    certification: Mapping[str, Any]
    canonical_hash: str
    presentation_hash: str
    review_hash: str
    certification_hash: str
    narrative_hash: str
    status: str
    version: int
    created: str
    reviewer: str
    metadata: Mapping[str, Any]

    def to_record(self) -> dict[str, Any]:
        """Serialize a freeze file. Does not rewrite Narrative."""
        return {
            "case_id": self.case_id,
            "presentation": thaw_mapping(self.presentation),
            "certification": thaw_mapping(self.certification),
            "canonical_hash": self.canonical_hash,
            "presentation_hash": self.presentation_hash,
            "review_hash": self.review_hash,
            "certification_hash": self.certification_hash,
            "narrative_hash": self.narrative_hash,
            "status": self.status,
            "version": self.version,
            "created": self.created,
            "reviewer": self.reviewer,
            "metadata": thaw_mapping(self.metadata),
        }

    @classmethod
    def from_record(cls, payload: Mapping[str, Any]) -> GoldenCase:
        """Rehydrate a frozen Golden Case. Presentation is copied, not rewritten."""
        presentation = payload.get("presentation")
        certification = payload.get("certification")
        metadata = payload.get("metadata")
        if not isinstance(presentation, Mapping) or not isinstance(certification, Mapping):
            raise ValueError("golden_case_incomplete")
        return cls(
            case_id=str(payload.get("case_id") or ""),
            presentation=freeze_mapping(dict(presentation)),  # type: ignore[arg-type]
            certification=freeze_mapping(dict(certification)),  # type: ignore[arg-type]
            canonical_hash=str(payload.get("canonical_hash") or ""),
            presentation_hash=str(payload.get("presentation_hash") or ""),
            review_hash=str(payload.get("review_hash") or ""),
            certification_hash=str(payload.get("certification_hash") or ""),
            narrative_hash=str(payload.get("narrative_hash") or ""),
            status=str(payload.get("status") or STATUS_FROZEN),
            version=int(payload.get("version") or 0),
            created=str(payload.get("created") or ""),
            reviewer=str(payload.get("reviewer") or ""),
            metadata=freeze_mapping(dict(metadata) if isinstance(metadata, Mapping) else {}),  # type: ignore[arg-type]
        )
