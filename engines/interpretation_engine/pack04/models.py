"""
Pack 04 Interpretation models — narrative aggregate (immutable).

Distinct from legacy ``legacy_builder.InterpretationResult`` used by production
``InterpretationEngine.run(RuleContext)``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Generic, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class EngineResult(Generic[T]):
    """Pack 04 ``Result<T>`` wrapper."""

    success: bool
    value: T | None = None
    warnings: list[str] = field(default_factory=list)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    trace: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InterpretationMetadata:
    """Metadata for one interpretation run."""

    interpretation_id: str = ""
    analysis_id: str = ""
    version: str = "1.0"
    engine_version: str = "pack04-1.0.0"
    language: str = "vi"
    generated_at: str = ""
    duration_ms: float = 0.0


@dataclass(slots=True)
class NarrativeSentence:
    """One rendered narrative sentence."""

    sentence_id: str
    section: str
    template_id: str
    text: str
    placeholders: dict[str, str] = field(default_factory=dict)
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 0.0
    rule_id: str = ""


@dataclass(slots=True)
class InterpretationSection:
    """One Pack 04 interpretation section."""

    section_id: str
    title: str
    sentences: list[NarrativeSentence] = field(default_factory=list)
    summary: str = ""

    @property
    def text(self) -> str:
        """Joined sentence text for the section."""
        if self.summary:
            return self.summary
        return " ".join(s.text for s in self.sentences if s.text)


@dataclass(slots=True)
class NarrativeInterpretationResult:
    """
    Pack 04 InterpretationResult aggregate.

    Canonical narrative output for AnalysisResult → narrative pipeline.
    """

    metadata: InterpretationMetadata = field(default_factory=InterpretationMetadata)
    overview: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("overview", "Tổng quan")
    )
    strength: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("strength", "Thân vượng nhược")
    )
    pattern: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("pattern", "Cách cục")
    )
    useful_god: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("useful_god", "Dụng thần")
    )
    ten_gods: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("ten_gods", "Thập thần")
    )
    five_elements: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("five_elements", "Ngũ hành")
    )
    season: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("season", "Khí mùa")
    )
    temperature: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("temperature", "Khí hậu")
    )
    summary: InterpretationSection = field(
        default_factory=lambda: InterpretationSection("summary", "Kết luận")
    )
    evidence_refs: list[str] = field(default_factory=list)
    matched_rules: list[str] = field(default_factory=list)
    success: bool = True

    def sections(self) -> list[InterpretationSection]:
        """Return ordered Pack 04 sections."""
        return [
            self.overview,
            self.strength,
            self.pattern,
            self.useful_god,
            self.ten_gods,
            self.five_elements,
            self.season,
            self.temperature,
            self.summary,
        ]

    def to_dict(self) -> dict[str, Any]:
        """Serialize aggregate for diagnostics and reports."""
        return {
            "success": self.success,
            "metadata": {
                "interpretation_id": self.metadata.interpretation_id,
                "analysis_id": self.metadata.analysis_id,
                "version": self.metadata.version,
                "engine_version": self.metadata.engine_version,
                "language": self.metadata.language,
                "generated_at": self.metadata.generated_at,
                "duration_ms": self.metadata.duration_ms,
            },
            "sections": {
                section.section_id: {
                    "title": section.title,
                    "summary": section.summary or section.text,
                    "sentences": [
                        {
                            "sentence_id": s.sentence_id,
                            "text": s.text,
                            "template_id": s.template_id,
                            "rule_id": s.rule_id,
                            "placeholders": dict(s.placeholders),
                            "evidence_ids": list(s.evidence_ids),
                            "confidence": s.confidence,
                        }
                        for s in section.sentences
                    ],
                }
                for section in self.sections()
            },
            "evidence_refs": list(self.evidence_refs),
            "matched_rules": list(self.matched_rules),
        }


def utc_now_iso() -> str:
    """Return UTC timestamp in ISO-8601."""
    return datetime.now(timezone.utc).isoformat()
