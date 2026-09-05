"""Canonical Pack 07 runtime contract models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from engines.detailed_interpretation_engine.codec import as_enum, as_str, as_str_tuple
from engines.detailed_interpretation_engine.constants import SCHEMA_RUNTIME_CONTRACT
from engines.detailed_interpretation_engine.domains import DomainSection
from engines.detailed_interpretation_engine.enums import ConsultingOperation, NarrativeLayer
from engines.detailed_interpretation_engine.evidence import InterpretationSection
from engines.detailed_interpretation_engine.narrative import NarrativeSection
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult, OptimizationResult
from engines.detailed_interpretation_engine.temporal import TemporalSection
from engines.detailed_interpretation_engine.value_objects import (
    ChartIdentity,
    Mc01Reference,
    RuntimeMetadata,
)


@dataclass(frozen=True, slots=True)
class ChartHandle:
    """Identity-only chart handle. Not a second BaZi engine."""

    chart_id: str = ""
    calendar_system_ref: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ChartHandle:
        """Rebuild a chart handle."""
        payload = data or {}
        return cls(
            chart_id=as_str(payload.get("chart_id")),
            calendar_system_ref=as_str(payload.get("calendar_system_ref")),
        )


@dataclass(frozen=True, slots=True)
class CanonicalRuntimeResult:
    """Published Pack 07 analysis. One analysis, one contract."""

    identity: ChartIdentity = field(default_factory=ChartIdentity)
    chart: ChartHandle = field(default_factory=ChartHandle)
    mc01: Mc01Reference = field(default_factory=Mc01Reference)
    interpretation: InterpretationSection = field(default_factory=InterpretationSection)
    domains: DomainSection = field(default_factory=DomainSection)
    temporal: TemporalSection = field(default_factory=TemporalSection)
    optimization: OptimizationResult = field(default_factory=LifeOptimizationResult)
    narrative: NarrativeSection = field(default_factory=NarrativeSection)
    metadata: RuntimeMetadata = field(default_factory=RuntimeMetadata)
    mc01_snapshot: str | None = None
    context_ref: str = ""

    @property
    def analysis_id(self) -> str:
        """Single analysis identity across layers."""
        return self.metadata.analysis_id or self.identity.analysis_id

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CanonicalRuntimeResult:
        """Rebuild the published runtime result."""
        payload = data or {}
        identity = ChartIdentity.from_dict(
            payload.get("identity") if isinstance(payload.get("identity"), Mapping) else None
        )
        metadata = RuntimeMetadata.from_dict(
            payload.get("metadata") if isinstance(payload.get("metadata"), Mapping) else None
        )
        analysis_id = metadata.analysis_id or identity.analysis_id or as_str(payload.get("analysis_id"))
        if analysis_id and identity.analysis_id != analysis_id:
            identity = ChartIdentity(
                analysis_id=analysis_id,
                chart_id=identity.chart_id,
                person_label_ref=identity.person_label_ref,
                birth_civil=identity.birth_civil,
                calendar_system_ref=identity.calendar_system_ref,
                gender_or_party_ref=identity.gender_or_party_ref,
                hour_completeness=identity.hour_completeness,
                timezone_ref=identity.timezone_ref,
            )
        if analysis_id and metadata.analysis_id != analysis_id:
            metadata = RuntimeMetadata(
                contract_version=metadata.contract_version,
                schema_version=metadata.schema_version,
                ruleset_version=metadata.ruleset_version,
                composer_version=metadata.composer_version,
                analysis_id=analysis_id,
                created_at=metadata.created_at,
                locale=metadata.locale,
                requested_layers=metadata.requested_layers,
                confidence_summary=metadata.confidence_summary,
                source_versions=dict(metadata.source_versions),
                content_hash=metadata.content_hash,
            )
        snapshot = payload.get("mc01_snapshot")
        return cls(
            identity=identity,
            chart=ChartHandle.from_dict(
                payload.get("chart") if isinstance(payload.get("chart"), Mapping) else None
            ),
            mc01=Mc01Reference.from_dict(
                payload.get("mc01") if isinstance(payload.get("mc01"), Mapping) else None
            ),
            interpretation=InterpretationSection.from_dict(
                payload.get("interpretation")
                if isinstance(payload.get("interpretation"), Mapping)
                else None
            ),
            domains=DomainSection.from_dict(
                payload.get("domains") if isinstance(payload.get("domains"), Mapping) else None
            ),
            temporal=TemporalSection.from_dict(
                payload.get("temporal") if isinstance(payload.get("temporal"), Mapping) else None
            ),
            optimization=LifeOptimizationResult.from_dict(
                payload.get("optimization")
                if isinstance(payload.get("optimization"), Mapping)
                else None
            ),
            narrative=NarrativeSection.from_dict(
                payload.get("narrative") if isinstance(payload.get("narrative"), Mapping) else None
            ),
            metadata=metadata,
            mc01_snapshot=str(snapshot) if snapshot is not None else None,
            context_ref=as_str(payload.get("context_ref")),
        )


CanonicalAnalysisResult = CanonicalRuntimeResult


@dataclass(frozen=True, slots=True)
class CanonicalExportModel:
    """Projection for PDF / DOCX / future PPT / HTML. Not a second truth."""

    analysis_id: str = ""
    contract_ref: str = SCHEMA_RUNTIME_CONTRACT
    selected_layer: NarrativeLayer = NarrativeLayer.COMMERCIAL
    section_order: tuple[str, ...] = ()
    included_block_ids: tuple[str, ...] = ()
    locale: str = "vi"

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CanonicalExportModel:
        """Rebuild an export projection."""
        payload = data or {}
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            contract_ref=as_str(payload.get("contract_ref"), SCHEMA_RUNTIME_CONTRACT),
            selected_layer=as_enum(
                NarrativeLayer,
                payload.get("selected_layer"),
                NarrativeLayer.COMMERCIAL,
            ),
            section_order=as_str_tuple(payload.get("section_order")),
            included_block_ids=as_str_tuple(payload.get("included_block_ids")),
            locale=as_str(payload.get("locale"), "vi"),
        )


@dataclass(frozen=True, slots=True)
class CanonicalAPIModel:
    """Stable machine envelope around CanonicalRuntimeResult."""

    analysis_id: str = ""
    contract: CanonicalRuntimeResult = field(default_factory=CanonicalRuntimeResult)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CanonicalAPIModel:
        """Rebuild the API envelope."""
        payload = data or {}
        contract_raw = payload.get("contract")
        contract = CanonicalRuntimeResult.from_dict(
            contract_raw if isinstance(contract_raw, Mapping) else payload
        )
        return cls(
            analysis_id=as_str(payload.get("analysis_id"), contract.analysis_id),
            contract=contract,
        )


@dataclass(frozen=True, slots=True)
class CanonicalConsultingModel:
    """Consulting projection. Dialogue may filter; it may not re-analyze."""

    analysis_id: str = ""
    contract_ref: str = SCHEMA_RUNTIME_CONTRACT
    default_layer: NarrativeLayer = NarrativeLayer.EXPERT
    allowed_operations: tuple[ConsultingOperation, ...] = (
        ConsultingOperation.RETRIEVE_BLOCK,
        ConsultingOperation.RETRIEVE_TRACE,
        ConsultingOperation.RETRIEVE_EVIDENCE,
        ConsultingOperation.RETRIEVE_OPTIMIZATION_ACTION,
    )
    forbidden_operations: tuple[ConsultingOperation, ...] = (
        ConsultingOperation.RECOMPUTE_PATTERN,
        ConsultingOperation.RERANK_EVIDENCE,
        ConsultingOperation.INVENT_ACTION,
        ConsultingOperation.MUTATE_CONTRACT,
    )

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> CanonicalConsultingModel:
        """Rebuild the consulting projection."""
        payload = data or {}
        allowed_raw = payload.get("allowed_operations")
        forbidden_raw = payload.get("forbidden_operations")
        allowed = (
            tuple(
                as_enum(ConsultingOperation, item, ConsultingOperation.RETRIEVE_BLOCK)
                for item in allowed_raw
            )
            if allowed_raw
            else cls().allowed_operations
        )
        forbidden = (
            tuple(
                as_enum(ConsultingOperation, item, ConsultingOperation.MUTATE_CONTRACT)
                for item in forbidden_raw
            )
            if forbidden_raw
            else cls().forbidden_operations
        )
        return cls(
            analysis_id=as_str(payload.get("analysis_id")),
            contract_ref=as_str(payload.get("contract_ref"), SCHEMA_RUNTIME_CONTRACT),
            default_layer=as_enum(
                NarrativeLayer,
                payload.get("default_layer"),
                NarrativeLayer.EXPERT,
            ),
            allowed_operations=allowed,
            forbidden_operations=forbidden,
        )
