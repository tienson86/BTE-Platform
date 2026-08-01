"""Sentence Engine metadata models.

Describes sentence *references* only.
No sentence library content. No natural language text.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.sentence_error import SentenceEngineError


@dataclass(frozen=True, slots=True)
class SentenceRef:
    """Immutable identifier for a sentence reference.

    Holds structural identity only — never sentence body text.
    """

    ref_id: str
    version: str = "0.0.0"
    domain: str = ""
    section: str = ""
    locale: str = ""
    status: str = "draft"
    priority: int = 0
    tags: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate structural sentence reference integrity."""
        return bool(self.ref_id and self.version)


@dataclass(frozen=True, slots=True)
class SentenceCandidate:
    """Candidate sentence reference with ranking score shell.

    Score is structural priority metadata, not generated language quality.
    """

    ref: SentenceRef
    score: float = 0.0
    rank: int | None = None
    reasons: tuple[str, ...] = ()

    def validate(self) -> bool:
        """Validate candidate structural integrity."""
        return self.ref.validate()


@dataclass(frozen=True, slots=True)
class SentenceComposition:
    """Ordered composition of sentence references.

    Contains reference identifiers only — no rendered natural language.
    """

    composition_id: str
    ref_ids: tuple[str, ...] = ()
    candidates: tuple[SentenceCandidate, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> bool:
        """Validate composition structural integrity."""
        if not self.composition_id:
            return False
        if self.candidates and self.ref_ids:
            candidate_ids = tuple(item.ref.ref_id for item in self.candidates)
            if candidate_ids != self.ref_ids:
                return False
        return True


class Metadata:
    """Normalize sentence-reference metadata without loading a sentence library."""

    def from_ref(self, ref: SentenceRef) -> dict[str, Any]:
        """Return a normalized metadata dictionary for a sentence reference."""
        metadata = dict(ref.metadata)
        metadata.setdefault("ref_id", ref.ref_id)
        metadata.setdefault("version", ref.version)
        metadata.setdefault("domain", ref.domain)
        metadata.setdefault("section", ref.section)
        metadata.setdefault("locale", ref.locale)
        metadata.setdefault("status", ref.status)
        metadata.setdefault("priority", ref.priority)
        metadata.setdefault("tags", list(ref.tags))
        metadata.setdefault("dependencies", list(ref.dependencies))
        return metadata

    def from_composition(self, composition: SentenceComposition) -> dict[str, Any]:
        """Return normalized metadata for a composition shell."""
        metadata = dict(composition.metadata)
        metadata.setdefault("composition_id", composition.composition_id)
        metadata.setdefault("ref_ids", list(composition.ref_ids))
        metadata.setdefault("candidate_count", len(composition.candidates))
        return metadata

    def from_mapping(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Extract metadata from a flat or nested sentence-ref mapping."""
        if "metadata" in payload and isinstance(payload["metadata"], Mapping):
            metadata = dict(payload["metadata"])
            for key in ("ref_id", "version", "domain", "section", "locale", "status"):
                if key in payload and key not in metadata:
                    metadata[key] = payload[key]
            return metadata
        if "ref_id" in payload or "composition_id" in payload:
            return dict(payload)
        raise SentenceEngineError("sentence_metadata_payload_unsupported")
