"""Published Interpretation Foundation contracts (IE-1). No textual content."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.interpretation_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    ENGINE_ID,
    INTERPRETATION_CONTRACT_ID,
    INTERPRETATION_VERSION,
    PUBLISHED_CONTEXT_INPUTS,
    PUBLISHED_CONTRACTS,
    RESULT_STATUS_EMPTY,
)


@dataclass(frozen=True, slots=True)
class InterpretationMetadata:
    """Version and upstream identity metadata. Not consultant copy."""

    interpretation_version: str
    schema_version: str
    analysis_pipeline_version: str | None = None
    decision_pipeline_version: str | None = None
    luck_pipeline_version: str | None = None
    module_ids: tuple[str, ...] = ()
    extras: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata."""
        return {
            "interpretation_version": self.interpretation_version,
            "schema_version": self.schema_version,
            "analysis_pipeline_version": self.analysis_pipeline_version,
            "decision_pipeline_version": self.decision_pipeline_version,
            "luck_pipeline_version": self.luck_pipeline_version,
            "module_ids": list(self.module_ids),
            "extras": dict(self.extras),
        }


@dataclass(frozen=True, slots=True)
class InterpretationReference:
    """Pointer to an upstream field. Holds no prose."""

    reference_id: str
    source: str
    field_path: str
    value_ref: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize a reference contract."""
        return {
            "reference_id": self.reference_id,
            "source": self.source,
            "field_path": self.field_path,
            "value_ref": self.value_ref,
        }


@dataclass(frozen=True, slots=True)
class InterpretationParagraph:
    """Structural paragraph slot. No sentence body."""

    paragraph_id: str
    chapter_id: str
    placeholder_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize a paragraph contract."""
        return {
            "paragraph_id": self.paragraph_id,
            "chapter_id": self.chapter_id,
            "placeholder_ids": list(self.placeholder_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class InterpretationChapter:
    """Structural chapter slot. No narrative."""

    chapter_id: str
    section_id: str
    paragraph_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize a chapter contract."""
        return {
            "chapter_id": self.chapter_id,
            "section_id": self.section_id,
            "paragraph_ids": list(self.paragraph_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class InterpretationSection:
    """Structural section slot bound to a registry module. No templates."""

    section_id: str
    module_id: str
    chapter_ids: tuple[str, ...] = ()
    reference_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize a section contract."""
        return {
            "section_id": self.section_id,
            "module_id": self.module_id,
            "chapter_ids": list(self.chapter_ids),
            "reference_ids": list(self.reference_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class InterpretationContext:
    """Published Interpretation Context contract. Snapshots only."""

    interpretation_version: str
    analysis_snapshot: Mapping[str, Any]
    decision_snapshot: Mapping[str, Any]
    luck_snapshot: Mapping[str, Any]
    published_outputs: tuple[str, ...] = ()
    metadata: InterpretationMetadata | None = None
    status: str = "ready"

    def to_dict(self) -> dict[str, Any]:
        """Serialize the context contract."""
        return {
            "interpretation_version": self.interpretation_version,
            "analysis_snapshot": dict(self.analysis_snapshot),
            "decision_snapshot": dict(self.decision_snapshot),
            "luck_snapshot": dict(self.luck_snapshot),
            "published_outputs": list(self.published_outputs),
            "metadata": None if self.metadata is None else self.metadata.to_dict(),
            "status": self.status,
        }


@dataclass(slots=True)
class CanonicalInterpretationResult:
    """Empty official Interpretation result shell. No generated content."""

    interpretation_version: str = INTERPRETATION_VERSION
    engine_id: str = ENGINE_ID
    success: bool = True
    status: str = RESULT_STATUS_EMPTY
    context: dict[str, Any] | None = None
    sections: tuple[dict[str, Any], ...] = ()
    chapters: tuple[dict[str, Any], ...] = ()
    paragraphs: tuple[dict[str, Any], ...] = ()
    references: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] | None = None
    diagnostics: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the empty canonical interpretation result."""
        return {
            "interpretation_version": self.interpretation_version,
            "engine_id": self.engine_id,
            "success": self.success,
            "status": self.status,
            "context": self.context,
            "sections": list(self.sections),
            "chapters": list(self.chapters),
            "paragraphs": list(self.paragraphs),
            "references": list(self.references),
            "metadata": self.metadata,
            "diagnostics": list(self.diagnostics),
            "errors": list(self.errors),
        }


def interpretation_foundation_contract() -> dict[str, Any]:
    """Return the published Interpretation Foundation field contract."""
    return {
        "contract_id": INTERPRETATION_CONTRACT_ID,
        "engine_id": ENGINE_ID,
        "interpretation_version": INTERPRETATION_VERSION,
        "inputs": list(PUBLISHED_CONTEXT_INPUTS),
        "contracts": list(PUBLISHED_CONTRACTS),
        "modules": list(CANONICAL_MODULE_ORDER),
        "text_generation": False,
        "reports": False,
        "ai": False,
        "packages_loaded": False,
    }


def empty_interpretation_result(
    *,
    context: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CanonicalInterpretationResult:
    """Build the IE-1 empty result shell."""
    return CanonicalInterpretationResult(
        context=None if context is None else dict(context),
        metadata=None if metadata is None else dict(metadata),
        diagnostics=("IE1-EMPTY-SHELL",),
    )
