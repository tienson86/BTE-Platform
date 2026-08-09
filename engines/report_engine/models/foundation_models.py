"""Runtime Report Foundation models. Structure only. No rendering."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.report_engine.foundation_constants import (
    PLACEHOLDER_STATUS_UNBOUND,
    REPORT_VERSION,
    RESULT_STATUS_EMPTY,
)


@dataclass(slots=True)
class PlaceholderModel:
    """Unbound placeholder identity for a future layout engine."""

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
class AssetModel:
    """Runtime asset identity. No binary payload."""

    asset_id: str
    asset_type: str
    source_ref: str | None = None
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the asset model."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "source_ref": self.source_ref,
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class BlockModel:
    """Runtime block container. Empty body in RE-1."""

    block_id: str
    section_id: str
    placeholder_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the block model."""
        return {
            "block_id": self.block_id,
            "section_id": self.section_id,
            "placeholder_ids": list(self.placeholder_ids),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class SectionModel:
    """Runtime section container bound to a registry module."""

    section_id: str
    module_id: str
    block_ids: tuple[str, ...] = ()
    asset_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the section model."""
        return {
            "section_id": self.section_id,
            "module_id": self.module_id,
            "block_ids": list(self.block_ids),
            "asset_ids": list(self.asset_ids),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class DocumentModel:
    """Runtime document container. Empty body in RE-1."""

    document_id: str
    section_ids: tuple[str, ...] = ()
    asset_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the document model."""
        return {
            "document_id": self.document_id,
            "section_ids": list(self.section_ids),
            "asset_ids": list(self.asset_ids),
            "status": self.status,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class MetadataModel:
    """Runtime metadata for a report foundation run."""

    report_version: str = REPORT_VERSION
    schema_version: str = "2.0.0"
    analysis_pipeline_version: str | None = None
    decision_pipeline_version: str | None = None
    luck_pipeline_version: str | None = None
    interpretation_pipeline_version: str | None = None
    module_ids: tuple[str, ...] = ()
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the metadata model."""
        return {
            "report_version": self.report_version,
            "schema_version": self.schema_version,
            "analysis_pipeline_version": self.analysis_pipeline_version,
            "decision_pipeline_version": self.decision_pipeline_version,
            "luck_pipeline_version": self.luck_pipeline_version,
            "interpretation_pipeline_version": self.interpretation_pipeline_version,
            "module_ids": list(self.module_ids),
            "extras": dict(self.extras),
        }


@dataclass(slots=True)
class ResultModel:
    """Runtime result shell. Documents remain empty until later sprints."""

    report_version: str = REPORT_VERSION
    success: bool = True
    status: str = RESULT_STATUS_EMPTY
    document: DocumentModel | None = None
    sections: tuple[SectionModel, ...] = ()
    blocks: tuple[BlockModel, ...] = ()
    assets: tuple[AssetModel, ...] = ()
    placeholders: tuple[PlaceholderModel, ...] = ()
    metadata: MetadataModel | None = None
    extras: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the result model."""
        return {
            "report_version": self.report_version,
            "success": self.success,
            "status": self.status,
            "document": None if self.document is None else self.document.to_dict(),
            "sections": [item.to_dict() for item in self.sections],
            "blocks": [item.to_dict() for item in self.blocks],
            "assets": [item.to_dict() for item in self.assets],
            "placeholders": [item.to_dict() for item in self.placeholders],
            "metadata": None if self.metadata is None else self.metadata.to_dict(),
            "extras": dict(self.extras),
        }
