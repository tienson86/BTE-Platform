"""Published Report Foundation contracts (RE-1). No rendering or export."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.report_engine.foundation_constants import (
    CANONICAL_MODULE_ORDER,
    ENGINE_ID,
    PUBLISHED_CONTEXT_INPUTS,
    PUBLISHED_CONTRACTS,
    REPORT_CONTRACT_ID,
    REPORT_VERSION,
    RESULT_STATUS_EMPTY,
)


@dataclass(frozen=True, slots=True)
class ReportMetadata:
    """Version and upstream identity metadata. Not presentation copy."""

    report_version: str
    schema_version: str
    analysis_pipeline_version: str | None = None
    decision_pipeline_version: str | None = None
    luck_pipeline_version: str | None = None
    interpretation_pipeline_version: str | None = None
    module_ids: tuple[str, ...] = ()
    extras: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize metadata."""
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


@dataclass(frozen=True, slots=True)
class ReportAsset:
    """Structural asset identity. Holds no binary or rendered payload."""

    asset_id: str
    asset_type: str
    source_ref: str | None = None
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize an asset contract."""
        return {
            "asset_id": self.asset_id,
            "asset_type": self.asset_type,
            "source_ref": self.source_ref,
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class ReportBlock:
    """Structural block slot. No formatted body."""

    block_id: str
    section_id: str
    placeholder_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize a block contract."""
        return {
            "block_id": self.block_id,
            "section_id": self.section_id,
            "placeholder_ids": list(self.placeholder_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class ReportSection:
    """Structural section slot bound to a registry module. No layout."""

    section_id: str
    module_id: str
    block_ids: tuple[str, ...] = ()
    asset_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize a section contract."""
        return {
            "section_id": self.section_id,
            "module_id": self.module_id,
            "block_ids": list(self.block_ids),
            "asset_ids": list(self.asset_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class ReportDocument:
    """Structural document slot. No pages, styles, or export bytes."""

    document_id: str
    section_ids: tuple[str, ...] = ()
    asset_ids: tuple[str, ...] = ()
    status: str = RESULT_STATUS_EMPTY

    def to_dict(self) -> dict[str, Any]:
        """Serialize a document contract."""
        return {
            "document_id": self.document_id,
            "section_ids": list(self.section_ids),
            "asset_ids": list(self.asset_ids),
            "status": self.status,
        }


@dataclass(frozen=True, slots=True)
class ReportContext:
    """Published Report Context contract. Snapshots only."""

    report_version: str
    analysis_snapshot: Mapping[str, Any]
    decision_snapshot: Mapping[str, Any]
    luck_snapshot: Mapping[str, Any]
    interpretation_snapshot: Mapping[str, Any]
    published_outputs: tuple[str, ...] = ()
    metadata: ReportMetadata | None = None
    status: str = "ready"

    def to_dict(self) -> dict[str, Any]:
        """Serialize the context contract."""
        return {
            "report_version": self.report_version,
            "analysis_snapshot": dict(self.analysis_snapshot),
            "decision_snapshot": dict(self.decision_snapshot),
            "luck_snapshot": dict(self.luck_snapshot),
            "interpretation_snapshot": dict(self.interpretation_snapshot),
            "published_outputs": list(self.published_outputs),
            "metadata": None if self.metadata is None else self.metadata.to_dict(),
            "status": self.status,
        }


@dataclass(slots=True)
class CanonicalReportResult:
    """Empty official Report result shell. No rendered content."""

    report_version: str = REPORT_VERSION
    engine_id: str = ENGINE_ID
    success: bool = True
    status: str = RESULT_STATUS_EMPTY
    context: dict[str, Any] | None = None
    document: dict[str, Any] | None = None
    sections: tuple[dict[str, Any], ...] = ()
    blocks: tuple[dict[str, Any], ...] = ()
    assets: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] | None = None
    diagnostics: tuple[str, ...] = ()
    errors: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Serialize the empty canonical report result."""
        return {
            "report_version": self.report_version,
            "engine_id": self.engine_id,
            "success": self.success,
            "status": self.status,
            "context": self.context,
            "document": self.document,
            "sections": list(self.sections),
            "blocks": list(self.blocks),
            "assets": list(self.assets),
            "metadata": self.metadata,
            "diagnostics": list(self.diagnostics),
            "errors": list(self.errors),
        }


def report_foundation_contract() -> dict[str, Any]:
    """Return the published Report Foundation field contract."""
    return {
        "contract_id": REPORT_CONTRACT_ID,
        "engine_id": ENGINE_ID,
        "report_version": REPORT_VERSION,
        "inputs": list(PUBLISHED_CONTEXT_INPUTS),
        "contracts": list(PUBLISHED_CONTRACTS),
        "modules": list(CANONICAL_MODULE_ORDER),
        "rendering": False,
        "export": False,
        "formatting": False,
        "pdf": False,
        "docx": False,
        "html": False,
        "markdown": False,
        "packages_loaded": False,
    }


def empty_report_result(
    *,
    context: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> CanonicalReportResult:
    """Build the RE-1 empty result shell."""
    return CanonicalReportResult(
        context=None if context is None else dict(context),
        metadata=None if metadata is None else dict(metadata),
        diagnostics=("RE1-EMPTY-SHELL",),
    )
