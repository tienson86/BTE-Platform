"""Commercial Language Layer — contracts."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FeatureKind(str, Enum):
    """Customer feature consuming CLL."""

    IDENTITY = "IDENTITY"
    CAREER = "CAREER"
    EXECUTIVE = "EXECUTIVE"


class ParagraphIntent(str, Enum):
    """Deterministic pattern selection key — no randomness."""

    OBSERVATION = "OBSERVATION"
    CONTRAST = "CONTRAST"
    CONDITION = "CONDITION"
    PRESSURE_RESPONSE = "PRESSURE_RESPONSE"
    WORK_STYLE = "WORK_STYLE"
    ACTION = "ACTION"
    LIMITATION = "LIMITATION"
    CLOSING = "CLOSING"
    RECOGNITION = "RECOGNITION"
    ENVIRONMENT = "ENVIRONMENT"
    INSIGHT = "INSIGHT"
    SUPPORT = "SUPPORT"


class ParagraphStatus(str, Enum):
    """Realization status."""

    READY = "READY"
    PARTIAL = "PARTIAL"
    INSUFFICIENT = "INSUFFICIENT"


@dataclass(slots=True)
class CommercialLanguageInput:
    """Deterministic input to CLL — claim-plan derived, not engine dumps."""

    feature: FeatureKind
    section: str
    intent: ParagraphIntent
    claims: list[str] = field(default_factory=list)
    supporting_claims: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    question_context: str = "GENERAL"
    language: str = "vi"
    tone_profile: str = "consultant"
    actionability: str = ""
    memory_candidate: str = ""
    primary_theme: str = ""
    operating_style: str = ""
    capacity_cue: str = ""
    structure_cue: str = ""
    balance_cue: str = ""
    versions: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ConsultingParagraph:
    """Structured consulting paragraph before final prose join."""

    intent: ParagraphIntent
    recognition: str = ""
    meaning: str = ""
    implication: str = ""
    action: str = ""
    limitation: str = ""
    memory_line: str = ""
    source_claim_ids: list[str] = field(default_factory=list)
    status: ParagraphStatus = ParagraphStatus.READY
    prose: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Validation serialization."""
        return {
            "intent": self.intent.value,
            "recognition": self.recognition,
            "meaning": self.meaning,
            "implication": self.implication,
            "action": self.action,
            "limitation": self.limitation,
            "memory_line": self.memory_line,
            "source_claim_ids": list(self.source_claim_ids),
            "status": self.status.value,
            "prose": self.prose,
        }


@dataclass(slots=True)
class FeatureLanguageResult:
    """Full feature body realized by CLL."""

    sections: list[tuple[str, str, list[str]]]
    body: str
    recommendations: list[str]
    memory_line: str = ""
    diagnostics: dict[str, Any] = field(default_factory=dict)
