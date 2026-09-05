"""Shen Sha secondary-evidence engine. Deterministic; no LLM."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.constants import SCHEMA_SHEN_SHA
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.evidence import InterpretationSection, ShenShaEcosystem
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.shen_sha.clusters import evaluate_shen_sha_ecosystem
from engines.detailed_interpretation_engine.shen_sha.constants import WARNING_UNKNOWN_STAR
from engines.detailed_interpretation_engine.shen_sha.evaluate import evaluate_shen_sha
from engines.detailed_interpretation_engine.shen_sha.facts import extract_shen_sha_facts, has_shen_sha_facts
from engines.detailed_interpretation_engine.shen_sha.models import (
    ShenShaEcosystemResult,
    ShenShaInterpretationCollection,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue, TraceRef
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_pack07_context,
    validate_shen_sha_collection,
    validate_shen_sha_ecosystem,
)


def interpret_shen_sha(
    payload: Mapping[str, Any] | None,
    *,
    analysis_id: str = "",
) -> ShenShaInterpretationCollection:
    """Evaluate detected stars as secondary evidence. Does not detect stars."""
    facts = extract_shen_sha_facts(payload)
    items = tuple(evaluate_shen_sha(match, facts) for match in facts.matches)
    warnings = [WARNING_UNKNOWN_STAR] if facts.unknown_ids else []
    evidence_ids = tuple(item.evidence_ids[0] for item in items if item.evidence_ids)
    trace_ids = tuple(trace for item in items for trace in item.trace_ids)
    summary: tuple[str, ...]
    if not facts.available:
        state = EvaluationStatus.UNRESOLVED
        summary = ("source:unavailable",)
        confidence = ConfidenceValue(summary="unresolved")
    elif not facts.mc01_bound:
        state = EvaluationStatus.PARTIALLY_RESOLVED
        summary = ("source:shen_sha_engine", "mc01:not_bound")
        confidence = ConfidenceValue(summary="low")
    else:
        state = EvaluationStatus.RESOLVED
        summary = ("source:shen_sha_engine", "mc01:bound")
        confidence = ConfidenceValue(summary="moderate")
    if facts.unknown_ids:
        summary = summary + tuple(f"unknown:{item}" for item in facts.unknown_ids)
    return ShenShaInterpretationCollection(
        analysis_id=analysis_id,
        state=state,
        items=items,
        summary=summary,
        warnings=tuple(warnings),
        evidence_ids=evidence_ids,
        trace_ids=trace_ids,
        confidence=confidence,
    )


def bind_shen_sha_collection(
    context: CanonicalAnalysisContext,
    collection: ShenShaInterpretationCollection,
    ecosystem: ShenShaEcosystemResult | None = None,
) -> CanonicalAnalysisContext:
    """Publish individual and ecosystem onto interpretation.shen_sha."""
    eco = ecosystem or ShenShaEcosystemResult(analysis_id=collection.analysis_id)
    finding_ids = tuple(item.shen_sha_id for item in collection.items) + tuple(
        item.cluster_id for item in eco.clusters if item.members
    )
    traces = collection.trace_ids + eco.trace_ids
    evidence = collection.evidence_ids + eco.evidence_ids
    shell = ShenShaEcosystem(
        schema_version=SCHEMA_SHEN_SHA,
        status=collection.state,
        finding_ids=finding_ids,
        trace=TraceRef(trace_ids=traces, evidence_ids=evidence),
        individual=collection,
        ecosystem=eco,
    )
    section = InterpretationSection(
        ten_gods=context.runtime.interpretation.ten_gods,
        shen_sha=shell,
        evidence_priority=context.runtime.interpretation.evidence_priority,
        status=collection.state,
        confidence=collection.confidence,
        trace_ids=context.runtime.interpretation.trace_ids + traces,
    )
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, interpretation=section, metadata=cleared)
    payload = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(payload))
    runtime = replace(runtime, metadata=metadata)
    return replace(context, runtime=runtime, status=collection.state)


def interpret_and_bind_shen_sha(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context when identity exists, evaluate Shen Sha layers, bind result."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    if not has_shen_sha_facts(payload):
        return context
    facts = extract_shen_sha_facts(payload)
    collection = interpret_shen_sha(payload, analysis_id=context.analysis_id)
    assert_valid(validate_shen_sha_collection(collection))
    ecosystem = evaluate_shen_sha_ecosystem(collection, facts, analysis_id=context.analysis_id)
    assert_valid(validate_shen_sha_ecosystem(ecosystem, individual=collection))
    return bind_shen_sha_collection(context, collection, ecosystem)
