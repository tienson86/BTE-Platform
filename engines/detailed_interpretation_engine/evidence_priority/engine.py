"""Evidence Priority Engine. Ranks existing canonical evidence only."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.evidence import EvidencePriorityResult, InterpretationSection
from engines.detailed_interpretation_engine.evidence_priority.assemble import assemble_result
from engines.detailed_interpretation_engine.evidence_priority.collect import (
    collect_candidates,
    score_engine_grade,
)
from engines.detailed_interpretation_engine.evidence_priority.merge import merge_semantic_candidates
from engines.detailed_interpretation_engine.mc01 import snapshot_from_live_payload
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.validators import assert_valid, validate_evidence_priority_result, validate_pack07_context


def evaluate_evidence_priority(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> EvidencePriorityResult:
    """Collect, merge, and rank existing MC-01 and Pack 07 evidence."""
    snapshot = snapshot_from_live_payload(payload)
    candidates = collect_candidates(context, payload)
    merged = merge_semantic_candidates(candidates)
    return assemble_result(
        analysis_id=context.analysis_id,
        items=merged,
        mc01_grade=snapshot.grade if snapshot else "",
        score_engine_grade=score_engine_grade(payload),
    )


def bind_evidence_priority(
    context: CanonicalAnalysisContext,
    result: EvidencePriorityResult,
) -> CanonicalAnalysisContext:
    """Publish EvidencePriorityResult onto interpretation.evidence_priority."""
    current = context.runtime.interpretation
    section = InterpretationSection(
        ten_gods=current.ten_gods,
        shen_sha=current.shen_sha,
        evidence_priority=result,
        status=current.status,
        confidence=current.confidence,
        trace_ids=current.trace_ids + result.trace_ids,
    )
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, interpretation=section, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    evidence_ctx = replace(context.evidence, status=result.status, evidence=result)
    return replace(context, runtime=runtime, evidence=evidence_ctx)


def interpret_and_bind_evidence_priority(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context, rank evidence, bind the canonical result."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    result = evaluate_evidence_priority(context, payload)
    if result.status.value != "not_evaluated":
        assert_valid(validate_evidence_priority_result(result, context=context, payload=payload))
    return bind_evidence_priority(context, result)
