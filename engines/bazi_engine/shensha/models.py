"""Production ShenSha detection result — identity plus provenance."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from engines.bazi_engine.shensha.formatter import evidence_text, presence_label


@dataclass(slots=True)
class ShenShaOccurrence:
    """One matched location of a canonical ShenSha."""

    pillar: str
    location: str
    target_value: str

    def to_dict(self) -> dict[str, str]:
        """Serialize one occurrence."""
        return {
            "pillar": self.pillar,
            "location": self.location,
            "target_value": self.target_value,
        }


@dataclass(slots=True)
class ShenShaMatch:
    """One published ShenSha with source, target, and all occurrences."""

    id: str
    canonical_name: str
    aliases: tuple[str, ...]
    source_type: str
    source_value: str
    target_type: str
    target_value: str
    occurrences: tuple[ShenShaOccurrence, ...]
    rule_source: str

    @property
    def pillar(self) -> str:
        """Primary pillar of the first occurrence."""
        return self.occurrences[0].pillar if self.occurrences else ""

    @property
    def location(self) -> str:
        """Primary stem/branch slot of the first occurrence."""
        return self.occurrences[0].location if self.occurrences else ""

    @property
    def presence_label(self) -> str:
        """Customer presence line, e.g. Có · trụ Tháng."""
        return presence_label(self.occurrences)

    @property
    def evidence_text(self) -> str:
        """Customer evidence line: source → target."""
        return evidence_text(
            self.source_type,
            self.source_value,
            self.occurrences,
            self.target_value,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize one match for API / Report / Portal copy."""
        return {
            "id": self.id,
            "canonical_name": self.canonical_name,
            "aliases": list(self.aliases),
            "source_type": self.source_type,
            "source_value": self.source_value,
            "target_type": self.target_type,
            "target_value": self.target_value,
            "pillar": self.pillar,
            "location": self.location,
            "rule_source": self.rule_source,
            "presence_label": self.presence_label,
            "evidence_text": self.evidence_text,
            "occurrences": [item.to_dict() for item in self.occurrences],
        }


@dataclass(slots=True)
class ShenShaDetectionResult:
    """Canonical ShenSha output. Names are a projection of matches."""

    matches: tuple[ShenShaMatch, ...] = field(default_factory=tuple)

    def canonical_names(self) -> list[str]:
        """Legacy list[str] projection — one name per logical star."""
        return [match.canonical_name for match in self.matches]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the detection result."""
        return {
            "matches": [match.to_dict() for match in self.matches],
            "names": self.canonical_names(),
        }
