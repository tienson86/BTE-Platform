"""Narrative Composer Engine. Consumes Pack 07 truth. Does not rewrite it."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.narrative import NarrativeResult, NarrativeSection
from engines.detailed_interpretation_engine.narrative_composer.evaluate import evaluate_narrative
from engines.detailed_interpretation_engine.narrative_composer.facts import collect_narrative_facts
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_narrative_result,
    validate_pack07_context,
)


def bind_narrative(
    context: CanonicalAnalysisContext,
    result: NarrativeResult,
) -> CanonicalAnalysisContext:
    """Publish NarrativeResult without writing into upstream objects."""
    domains = context.runtime.domains
    temporal = context.runtime.temporal
    interpretation = context.runtime.interpretation
    optimization = context.runtime.optimization
    section = NarrativeSection(
        graph=result.graph,
        result=result,
        executive_summary=result.executive_summary,
        layers=result.layers,
    )
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, narrative=section, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    narrative_ctx = replace(
        context.narrative,
        analysis_id=context.analysis_id,
        status=result.status,
        inputs=section,
    )
    bound = replace(context, runtime=runtime, narrative=narrative_ctx)
    if bound.runtime.domains is not domains:
        raise RuntimeError("narrative mutated domains")
    if bound.runtime.temporal is not temporal:
        raise RuntimeError("narrative mutated temporal")
    if bound.runtime.interpretation is not interpretation:
        raise RuntimeError("narrative mutated interpretation")
    if bound.runtime.optimization is not optimization:
        raise RuntimeError("narrative mutated optimization")
    return bound


def interpret_and_bind_narrative(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context, compose narrative, bind without mutating upstream."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    facts = collect_narrative_facts(context, payload)
    result = evaluate_narrative(facts)
    if result.status not in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        assert_valid(validate_narrative_result(result, context=context))
    return bind_narrative(context, result)
