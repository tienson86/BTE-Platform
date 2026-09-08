"""Result models for Number Energy Engine V1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class DigitType(str, Enum):
    """Internal digit classification from NUMBER_ENERGY_MASTER_KNOWLEDGE_V1."""

    GUA = "gua"
    MODIFIER = "modifier"


class EnergyState(str, Enum):
    """Canonical energy states plus the V1 undefined sentinel."""

    NORMAL = "NORMAL"
    HIDDEN = "HIDDEN"
    AMPLIFIED = "AMPLIFIED"
    REPEATED = "REPEATED"
    CONTROLLED = "CONTROLLED"
    NEUTRALIZED = "NEUTRALIZED"
    UNKNOWN_OR_NOT_DEFINED = "UNKNOWN_OR_NOT_DEFINED"


class PurposeContext(str, Enum):
    """Supported V1 purpose contexts."""

    PHONE_NUMBER = "phone_number"
    CAR_PLATE = "car_plate"
    MOTORBIKE_PLATE = "motorbike_plate"
    ID_NUMBER = "id_number"
    BANK_ACCOUNT = "bank_account"
    HOUSE_NUMBER = "house_number"
    GENERIC_NUMBER = "generic_number"


class Classification(str, Enum):
    """Frozen energy classes."""

    SUPPORTIVE = "supportive"
    SUPPORTIVE_STABILIZING = "supportive_stabilizing"
    CHALLENGING = "challenging"


@dataclass(slots=True)
class ClassifiedDigit:
    """One digit after Layer 2 classification."""

    index: int
    digit: int
    internal_type: str
    gua_or_field: str
    direction: str
    element: str | None
    group: str
    pair_role: str


@dataclass(slots=True)
class ParsedNumber:
    """Layer 1–2 parse result. ``raw_digits`` keeps the original digit order."""

    input_raw: str
    raw_digits: tuple[int, ...]
    classified_digits: tuple[ClassifiedDigit, ...]


@dataclass(slots=True)
class EnergyOccurrence:
    """One detected Du Niên occurrence."""

    occurrence_id: str
    source_span: tuple[int, int]
    source_digits: str
    pair_digits: str
    energy_id: str
    display_name: str
    strength_rank: int | None
    classification: str
    state: str
    via_modifier: int | None
    notes: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one occurrence."""
        return asdict(self)


@dataclass(slots=True)
class UndefinedSegment:
    """A span whose interaction is not frozen in V1."""

    source_span: tuple[int, int]
    source_digits: str
    state: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one undefined segment."""
        return asdict(self)


@dataclass(slots=True)
class SequenceSummary:
    """Aggregation without numeric scoring."""

    dominant_energy_ids: tuple[str, ...]
    strongest_rank: int | None
    repeated_energy_ids: tuple[str, ...]
    controlled_energy_ids: tuple[str, ...]
    challenging_without_control: tuple[str, ...]
    fu_wei_supported: bool
    approved_supportive_chain: bool

    def to_dict(self) -> dict[str, Any]:
        """Serialize sequence summary."""
        return asdict(self)


@dataclass(slots=True)
class CustomerNarrative:
    """Customer-facing Vietnamese copy with V1 safety bounds."""

    language: str
    system_name: str
    system_short_name: str
    summary: str
    paragraphs: tuple[str, ...]
    strengths: tuple[str, ...]
    watchouts: tuple[str, ...]
    purpose_focus: str
    health_disclaimer: str | None
    compatibility_note: str
    unknown_notice: str | None

    def to_dict(self) -> dict[str, Any]:
        """Serialize customer narrative."""
        return asdict(self)


@dataclass(slots=True)
class NumberEnergyResult:
    """Canonical engine result for one number string."""

    input_raw: str
    raw_digits: tuple[int, ...]
    classified_digits: tuple[ClassifiedDigit, ...]
    occurrences: tuple[EnergyOccurrence, ...]
    undefined_segments: tuple[UndefinedSegment, ...]
    sequence_state: str
    sequence_states: tuple[str, ...]
    approved_patterns: tuple[str, ...]
    purpose_context: str
    summary: SequenceSummary
    narrative: CustomerNarrative
    expert_notes: tuple[str, ...]
    knowledge_version: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        """Serialize for API / presentation layers."""
        return {
            "input_raw": self.input_raw,
            "raw_digits": list(self.raw_digits),
            "classified_digits": [asdict(item) for item in self.classified_digits],
            "occurrences": [item.to_dict() for item in self.occurrences],
            "undefined_segments": [item.to_dict() for item in self.undefined_segments],
            "sequence_state": self.sequence_state,
            "sequence_states": list(self.sequence_states),
            "approved_patterns": list(self.approved_patterns),
            "purpose_context": self.purpose_context,
            "summary": self.summary.to_dict(),
            "narrative": self.narrative.to_dict(),
            "expert_notes": list(self.expert_notes),
            "knowledge_version": self.knowledge_version,
            "system_name": "Bát Cực Linh Số",
            "system_short_name": "Năng lượng số",
        }
