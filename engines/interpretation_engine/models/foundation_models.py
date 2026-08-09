"""Runtime Interpretation Foundation models. Structure only. No prose."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.foundation_constants import (
    INTERPRETATION_VERSION,
    PLACEHOLDER_STATUS_UNBOUND,
    RESULT_STATUS_EMPTY,
)


@dataclass(slots=True)
class PlaceholderModel:
    """Unbound placeholder identity for a future sentence engine."""

    placeholder_id: str
    binding_path: str
    status: str = PLACEHOLDER_STATUS_UNBOUND
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the placeholder model."""
        return {
            "placeholder_id": self.placeholder_id,
            "binding_path": self.binding_path,
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ReferenceModel:
    """Runtime upstream reference. Value identity only."""

    reference_id: str
    source: str
    field_path: str
    value_ref: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the reference model."""
        return {
            "reference_id": self.reference_id,
            "source": self.source,
            "field_path": self.field_path,
            "value_ref": self.value_ref,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ParagraphModel:
    """Runtime paragraph container. Empty body in IE-1."""

    paragraph_id: str
    chapter_id: str
    placeholder_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the paragraph model."""
        return {
            "paragraph_id": self.paragraph_id,
            "chapter_id": self.chapter_id,
            "placeholder_ids": list(self.placeholder_ids),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ChapterModel:
    """Runtime chapter container. Empty body in IE-1."""

    chapter_id: str
    section_id: str
    paragraph_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the chapter model."""
        return {
            "chapter_id": self.chapter_id,
            "section_id": self.section_id,
            "paragraph_ids": list(self.paragraph_ids),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class SectionModel:
    """Runtime section container bound to a registry module."""

    section_id: str
    module_id: str
    chapter_ids: tuple[str, ...] = ()
    reference_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the section model."""
        return {
            "section_id": self.section_id,
            "module_id": self.module_id,
            "chapter_ids": list(self.chapter_ids),
            "reference_ids": list(self.reference_ids),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class MetadataModel:
    """Runtime metadata for an interpretation foundation run."""

    interpretation_version: str = INTERPRETATION_VERSION
    schema_version: str = "2.0.0"
    analysis_pipeline_version: str | None = None
    decision_pipeline_version: str | None = None
    luck_pipeline_version: str | None = None
    module_ids: tuple[str, ...] = ()
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the metadata model."""
        return {
            "interpretation_version": self.interpretation_version,
            "schema_version": self.schema_version,
            "analysis_pipeline_version": self.analysis_pipeline_version,
            "decision_pipeline_version": self.decision_pipeline_version,
            "luck_pipeline_version": self.luck_pipeline_version,
            "module_ids": list(self.module_ids),
            "extras": dict(self.extras),
        }


@dataclass(slots=True)
class ResultModel:
    """Runtime result shell. Sections remain empty until later sprints."""

    interpretation_version: str = INTERPRETATION_VERSION
    success: bool = True
    status: str = RESULT_STATUS_EMPTY
    sections: tuple[SectionModel, ...] = ()
    chapters: tuple[ChapterModel, ...] = ()
    paragraphs: tuple[ParagraphModel, ...] = ()
    references: tuple[ReferenceModel, ...] = ()
    placeholders: tuple[PlaceholderModel, ...] = ()
    metadata: MetadataModel | None = None
    extras: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the result model."""
        return {
            "interpretation_version": self.interpretation_version,
            "success": self.success,
            "status": self.status,
            "sections": [item.to_dict() for item in self.sections],
            "chapters": [item.to_dict() for item in self.chapters],
            "paragraphs": [item.to_dict() for item in self.paragraphs],
            "references": [item.to_dict() for item in self.references],
            "placeholders": [item.to_dict() for item in self.placeholders],
            "metadata": None if self.metadata is None else self.metadata.to_dict(),
            "extras": dict(self.extras),
        }
