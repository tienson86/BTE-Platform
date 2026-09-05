"""Factories for empty Pack 07 contract objects.

Factories instantiate frozen shells. They do not interpret.
"""

from __future__ import annotations

from datetime import datetime, timezone
from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.constants import DEFAULT_LOCALE, SCHEMA_RUNTIME_CONTRACT
from engines.detailed_interpretation_engine.context import InterpretationContext
from engines.detailed_interpretation_engine.context_layers import (
    CanonicalAnalysisContext,
    DomainContext,
    EvidenceContext,
    NarrativeContext,
    OptimizationContext,
    TemporalContext,
)
from engines.detailed_interpretation_engine.enums import ConsultingOperation, NarrativeLayer
from engines.detailed_interpretation_engine.runtime import (
    CanonicalAPIModel,
    CanonicalConsultingModel,
    CanonicalExportModel,
    CanonicalRuntimeResult,
    ChartHandle,
)
from engines.detailed_interpretation_engine.serialization import (
    compute_content_hash,
    serialize_runtime_result,
)
from engines.detailed_interpretation_engine.temporal import TemporalSection
from engines.detailed_interpretation_engine.upstream import (
    UpstreamStructuralRefs,
    extract_upstream_refs,
)
from engines.detailed_interpretation_engine.value_objects import (
    ChartIdentity,
    Mc01Reference,
    RuntimeMetadata,
)


def build_interpretation_context(
    analysis_id: str,
    *,
    chart_id: str = "",
    mingju_result_id: str = "",
    mingju_content_hash: str = "",
    locale: str = DEFAULT_LOCALE,
    requested_layers: tuple[str, ...] = (),
    mc01: Mc01Reference | None = None,
    pattern_ref: str = "",
    grade_ref: str = "",
    integrity_ref: str = "",
    strength_ref: str = "",
    useful_god_ref: str = "",
    temperature_ref: str = "",
    five_elements_ref: str = "",
    chart_identity: ChartIdentity | None = None,
) -> InterpretationContext:
    """Build an identity-only interpretation context."""
    resolved_mc01 = mc01 if mc01 is not None else Mc01Reference(
        mingju_result_id=mingju_result_id,
        content_hash=mingju_content_hash,
    )
    resolved_identity = chart_identity if chart_identity is not None else ChartIdentity(
        analysis_id=analysis_id,
        chart_id=chart_id,
    )
    if analysis_id and not resolved_identity.analysis_id:
        resolved_identity = replace(resolved_identity, analysis_id=analysis_id)
    return InterpretationContext(
        analysis_id=analysis_id,
        chart_id=chart_id,
        mingju_result_id=mingju_result_id or resolved_mc01.mingju_result_id,
        mingju_content_hash=mingju_content_hash or resolved_mc01.content_hash,
        locale=locale,
        requested_layers=requested_layers,
        mc01=resolved_mc01,
        pattern_ref=pattern_ref,
        grade_ref=grade_ref,
        integrity_ref=integrity_ref,
        strength_ref=strength_ref,
        useful_god_ref=useful_god_ref,
        temperature_ref=temperature_ref,
        five_elements_ref=five_elements_ref,
        chart_identity=resolved_identity,
    )


def build_evidence_context(analysis_id: str) -> EvidenceContext:
    """Prepare empty evidence containers. No ranking."""
    return EvidenceContext(analysis_id=analysis_id)


def build_domain_context(analysis_id: str) -> DomainContext:
    """Prepare empty natal domain containers. No domain logic."""
    return DomainContext(analysis_id=analysis_id)


def build_temporal_context(analysis_id: str) -> TemporalContext:
    """Prepare empty luck / interaction / temporal containers."""
    section = TemporalSection()
    return TemporalContext(
        analysis_id=analysis_id,
        luck=section.luck_activation,
        interaction=section.luck_interaction,
        temporal=section.temporal_activation,
        section=section,
    )


def build_optimization_context(analysis_id: str) -> OptimizationContext:
    """Prepare empty optimization inputs. No decisions."""
    return OptimizationContext(analysis_id=analysis_id)


def build_narrative_context(analysis_id: str) -> NarrativeContext:
    """Prepare empty narrative inputs. No composer."""
    return NarrativeContext(analysis_id=analysis_id)


def _context_ref_from_interpretation(interpretation: InterpretationContext) -> str:
    digest = compute_content_hash(
        {
            "analysis_id": interpretation.analysis_id,
            "chart_id": interpretation.chart_id,
            "pattern_ref": interpretation.pattern_ref,
            "grade_ref": interpretation.grade_ref,
            "integrity_ref": interpretation.integrity_ref,
            "strength_ref": interpretation.strength_ref,
            "useful_god_ref": interpretation.useful_god_ref,
            "temperature_ref": interpretation.temperature_ref,
            "five_elements_ref": interpretation.five_elements_ref,
            "mingju_result_id": interpretation.mingju_result_id,
        }
    )
    return f"ctx-{digest[:16]}"


def build_canonical_analysis_context(
    analysis_id: str = "",
    *,
    payload: Mapping[str, Any] | None = None,
    refs: UpstreamStructuralRefs | None = None,
) -> CanonicalAnalysisContext:
    """Assemble the canonical context chain. No reasoning."""
    snapshot = refs
    if snapshot is None and payload is not None:
        snapshot = extract_upstream_refs(payload)
    if snapshot is None:
        snapshot = UpstreamStructuralRefs(analysis_id=analysis_id)
    resolved_id = analysis_id or snapshot.analysis_id
    interpretation = build_interpretation_context(
        resolved_id,
        chart_id=snapshot.chart_id,
        mingju_result_id=snapshot.mingju_result_id,
        mingju_content_hash=snapshot.mingju_content_hash,
        locale=snapshot.locale,
        mc01=snapshot.mc01,
        pattern_ref=snapshot.pattern_ref,
        grade_ref=snapshot.grade_ref,
        integrity_ref=snapshot.integrity_ref,
        strength_ref=snapshot.strength_ref,
        useful_god_ref=snapshot.useful_god_ref,
        temperature_ref=snapshot.temperature_ref,
        five_elements_ref=snapshot.five_elements_ref,
        chart_identity=snapshot.chart_identity,
    )
    context_ref = _context_ref_from_interpretation(interpretation)
    runtime = empty_canonical_runtime_result(
        resolved_id,
        chart_id=snapshot.chart_id,
        locale=snapshot.locale,
        context_ref=context_ref,
        mc01=snapshot.mc01,
    )
    return CanonicalAnalysisContext(
        analysis_id=resolved_id,
        interpretation=interpretation,
        evidence=build_evidence_context(resolved_id),
        domain=build_domain_context(resolved_id),
        temporal=build_temporal_context(resolved_id),
        optimization=build_optimization_context(resolved_id),
        narrative=build_narrative_context(resolved_id),
        runtime=runtime,
        context_ref=context_ref,
    )


def empty_canonical_runtime_result(
    analysis_id: str,
    *,
    chart_id: str = "",
    locale: str = DEFAULT_LOCALE,
    created_at: str | None = None,
    context_ref: str = "",
    mc01: Mc01Reference | None = None,
) -> CanonicalRuntimeResult:
    """Instantiate a not-evaluated CanonicalRuntimeResult that serializes."""
    timestamp = created_at if created_at is not None else datetime.now(timezone.utc).isoformat()
    identity = ChartIdentity(analysis_id=analysis_id, chart_id=chart_id)
    metadata = RuntimeMetadata(
        analysis_id=analysis_id,
        created_at=timestamp,
        locale=locale,
    )
    resolved_mc01 = mc01 if mc01 is not None else Mc01Reference()
    draft = CanonicalRuntimeResult(
        identity=identity,
        chart=ChartHandle(chart_id=chart_id),
        mc01=resolved_mc01,
        metadata=metadata,
        context_ref=context_ref,
    )
    payload = serialize_runtime_result(draft)
    hashed = RuntimeMetadata(
        contract_version=metadata.contract_version,
        schema_version=metadata.schema_version,
        ruleset_version=metadata.ruleset_version,
        composer_version=metadata.composer_version,
        analysis_id=analysis_id,
        created_at=timestamp,
        locale=locale,
        requested_layers=metadata.requested_layers,
        confidence_summary=metadata.confidence_summary,
        source_versions=dict(metadata.source_versions),
        content_hash=compute_content_hash(payload),
    )
    return CanonicalRuntimeResult(
        identity=identity,
        chart=ChartHandle(chart_id=chart_id),
        mc01=resolved_mc01,
        metadata=hashed,
        context_ref=context_ref,
    )


def export_model_from_runtime(
    result: CanonicalRuntimeResult,
    *,
    layer: NarrativeLayer = NarrativeLayer.COMMERCIAL,
) -> CanonicalExportModel:
    """Project CanonicalExportModel from a published result. No new findings."""
    return CanonicalExportModel(
        analysis_id=result.analysis_id,
        contract_ref=SCHEMA_RUNTIME_CONTRACT,
        selected_layer=layer,
        locale=result.metadata.locale,
        included_block_ids=tuple(node.node_id for node in result.narrative.graph.nodes),
    )


def api_model_from_runtime(result: CanonicalRuntimeResult) -> CanonicalAPIModel:
    """Wrap CanonicalRuntimeResult as CanonicalAPIModel."""
    return CanonicalAPIModel(analysis_id=result.analysis_id, contract=result)


def consulting_model_from_runtime(result: CanonicalRuntimeResult) -> CanonicalConsultingModel:
    """Project CanonicalConsultingModel from a published result."""
    return CanonicalConsultingModel(
        analysis_id=result.analysis_id,
        default_layer=NarrativeLayer.EXPERT,
        allowed_operations=(
            ConsultingOperation.RETRIEVE_BLOCK,
            ConsultingOperation.RETRIEVE_TRACE,
            ConsultingOperation.RETRIEVE_EVIDENCE,
            ConsultingOperation.RETRIEVE_OPTIMIZATION_ACTION,
        ),
        forbidden_operations=(
            ConsultingOperation.RECOMPUTE_PATTERN,
            ConsultingOperation.RERANK_EVIDENCE,
            ConsultingOperation.INVENT_ACTION,
            ConsultingOperation.MUTATE_CONTRACT,
        ),
    )
