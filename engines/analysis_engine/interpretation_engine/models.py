"""Interpretation Engine domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

from engines.analysis_engine.runtime.models import (
    AnalysisResult,
    ConfidenceEvaluation,
    DiagnosticInfo,
    RuleEvidence,
)

CANONICAL_SECTIONS: tuple[str, ...] = (
    "overview",
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
    "luck",
    "recommendations",
)

REQUIRED_ANALYSIS_STAGES: tuple[str, ...] = (
    "strength",
    "temperature",
    "pattern",
    "useful_god",
    "ten_gods",
    "combination",
    "shensha",
    "luck",
    "summary",
)


@dataclass(slots=True)
class InterpretationContext:
    """Input contract for Interpretation Engine.

    Consumes published ``AnalysisResult`` only — never mutates it.
    """

    analysis_result: AnalysisResult
    chart: Mapping[str, Any] = field(default_factory=dict)
    knowledge_session: Any | None = None
    knowledge_version: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    request_id: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "chart", MappingProxyType(dict(self.chart)))
        if not self.request_id:
            self.request_id = self.analysis_result.request_id


@dataclass(slots=True, frozen=True)
class SelectedSentence:
    """Sentence candidate selected from the sentence library."""

    sentence_id: str
    section_id: str
    source_stage: str
    template_id: str
    priority: int
    match: Mapping[str, Any] = field(default_factory=dict)
    placeholders: tuple[str, ...] = ()
    required_placeholders: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "match", MappingProxyType(dict(self.match)))
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


@dataclass(slots=True, frozen=True)
class BoundTemplate:
    """Selected sentence with resolved template text."""

    sentence_id: str
    section_id: str
    source_stage: str
    template_id: str
    template_text: str
    priority: int
    placeholders: tuple[str, ...] = ()
    required_placeholders: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


@dataclass(slots=True, frozen=True)
class BoundSentence:
    """Sentence after placeholder substitution."""

    sentence_id: str
    section_id: str
    source_stage: str
    template_id: str
    text: str
    priority: int
    bound_values: Mapping[str, str] = field(default_factory=dict)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "bound_values",
            MappingProxyType(dict(self.bound_values)),
        )
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


@dataclass(slots=True, frozen=True)
class InterpretationParagraph:
    """Ordered paragraph within a section."""

    section_id: str
    sentences: tuple[BoundSentence, ...]
    text: str

    @property
    def sentence_texts(self) -> tuple[str, ...]:
        """Return plain sentence texts."""
        return tuple(item.text for item in self.sentences)


@dataclass(slots=True, frozen=True)
class InterpretationSection:
    """Published interpretive section."""

    section_id: str
    title: str
    paragraphs: tuple[InterpretationParagraph, ...]
    body: str
    sentence_ids: tuple[str, ...] = ()
    source_stages: tuple[str, ...] = ()


@dataclass(slots=True)
class InterpretationResult:
    """Immutable public output of the Interpretation Engine."""

    request_id: str
    sections: tuple[InterpretationSection, ...]
    overview: str
    confidence: ConfidenceEvaluation
    evidence: tuple[RuleEvidence, ...]
    diagnostics: tuple[DiagnosticInfo, ...]
    knowledge_version: str
    module_version: str = "1.0.0"
    summary: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "summary", MappingProxyType(dict(self.summary)))

    def section_map(self) -> Mapping[str, InterpretationSection]:
        """Return sections keyed by section_id."""
        return MappingProxyType({item.section_id: item for item in self.sections})

    def to_dict(self) -> dict[str, Any]:
        """Serialize for tests and downstream consumers."""
        return {
            "request_id": self.request_id,
            "overview": self.overview,
            "module_version": self.module_version,
            "knowledge_version": self.knowledge_version,
            "sections": [
                {
                    "section_id": section.section_id,
                    "title": section.title,
                    "body": section.body,
                    "sentence_ids": list(section.sentence_ids),
                    "source_stages": list(section.source_stages),
                    "paragraphs": [
                        {
                            "section_id": paragraph.section_id,
                            "text": paragraph.text,
                            "sentences": [
                                {
                                    "sentence_id": sentence.sentence_id,
                                    "section_id": sentence.section_id,
                                    "source_stage": sentence.source_stage,
                                    "template_id": sentence.template_id,
                                    "text": sentence.text,
                                    "priority": sentence.priority,
                                    "bound_values": dict(sentence.bound_values),
                                    "metadata": dict(sentence.metadata),
                                }
                                for sentence in paragraph.sentences
                            ],
                        }
                        for paragraph in section.paragraphs
                    ],
                }
                for section in self.sections
            ],
            "confidence": {
                "score": self.confidence.score,
                "level": self.confidence.level,
                "details": dict(self.confidence.details),
            },
            "evidence": [
                {
                    "rule_id": item.rule_id,
                    "version": item.version,
                    "category": item.category,
                    "priority": item.priority,
                    "reference": item.reference,
                    "details": dict(item.details),
                }
                for item in self.evidence
            ],
            "diagnostics": [
                {
                    "code": item.code,
                    "message": item.message,
                    "level": item.level,
                    "stage_id": item.stage_id,
                    "details": dict(item.details),
                }
                for item in self.diagnostics
            ],
            "summary": dict(self.summary),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> InterpretationResult:
        """Rebuild InterpretationResult from a serialized payload."""
        confidence_raw = payload.get("confidence") or {}
        sections: list[InterpretationSection] = []
        for section_raw in payload.get("sections", []):
            paragraphs: list[InterpretationParagraph] = []
            for paragraph_raw in section_raw.get("paragraphs", []):
                sentences = tuple(
                    BoundSentence(
                        sentence_id=item["sentence_id"],
                        section_id=item["section_id"],
                        source_stage=item["source_stage"],
                        template_id=item["template_id"],
                        text=item["text"],
                        priority=int(item.get("priority", 0)),
                        bound_values=dict(item.get("bound_values") or {}),
                        metadata=dict(item.get("metadata") or {}),
                    )
                    for item in paragraph_raw.get("sentences", [])
                )
                paragraphs.append(
                    InterpretationParagraph(
                        section_id=str(paragraph_raw.get("section_id") or ""),
                        sentences=sentences,
                        text=str(paragraph_raw.get("text") or ""),
                    )
                )
            sections.append(
                InterpretationSection(
                    section_id=str(section_raw["section_id"]),
                    title=str(section_raw.get("title") or ""),
                    paragraphs=tuple(paragraphs),
                    body=str(section_raw.get("body") or ""),
                    sentence_ids=tuple(section_raw.get("sentence_ids") or ()),
                    source_stages=tuple(section_raw.get("source_stages") or ()),
                )
            )
        return cls(
            request_id=str(payload.get("request_id") or ""),
            sections=tuple(sections),
            overview=str(payload.get("overview") or ""),
            confidence=ConfidenceEvaluation(
                score=confidence_raw.get("score"),
                level=confidence_raw.get("level"),
                details=dict(confidence_raw.get("details") or {}),
            ),
            evidence=tuple(
                RuleEvidence(
                    rule_id=item["rule_id"],
                    version=item.get("version", "1.0.0"),
                    category=item.get("category", ""),
                    priority=int(item.get("priority", 0)),
                    reference=item.get("reference", ""),
                    details=dict(item.get("details") or {}),
                )
                for item in payload.get("evidence", [])
            ),
            diagnostics=tuple(
                DiagnosticInfo(
                    code=item["code"],
                    message=item["message"],
                    level=item.get("level", "info"),
                    stage_id=item.get("stage_id"),
                    details=dict(item.get("details") or {}),
                )
                for item in payload.get("diagnostics", [])
            ),
            knowledge_version=str(payload.get("knowledge_version") or "1.0.0"),
            module_version=str(payload.get("module_version") or "1.0.0"),
            summary=dict(payload.get("summary") or {}),
        )
