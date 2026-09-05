"""Life Optimization Engine. Consumes Pack 07 truth. Does not rewrite it."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.life_optimization.evaluate import evaluate_life_optimization
from engines.detailed_interpretation_engine.life_optimization.facts import collect_life_optimization_facts
from engines.detailed_interpretation_engine.optimization import LifeOptimizationResult
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_life_optimization_result,
    validate_pack07_context,
)


def bind_life_optimization(
    context: CanonicalAnalysisContext,
    result: LifeOptimizationResult,
) -> CanonicalAnalysisContext:
    """Publish LifeOptimizationResult without writing into Domain or Temporal objects."""
    domains = context.runtime.domains
    temporal = context.runtime.temporal
    interpretation = context.runtime.interpretation
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, optimization=result, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    optimization_ctx = replace(
        context.optimization,
        analysis_id=result.analysis_id or context.analysis_id,
        status=result.state,
        inputs=result,
    )
    bound = replace(context, runtime=runtime, optimization=optimization_ctx)
    if bound.runtime.domains is not domains:
        raise RuntimeError("optimization mutated domains")
    if bound.runtime.temporal is not temporal:
        raise RuntimeError("optimization mutated temporal")
    if bound.runtime.interpretation is not interpretation:
        raise RuntimeError("optimization mutated interpretation")
    return bound


def interpret_and_bind_life_optimization(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context, evaluate Life Optimization, bind without mutating upstream."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    facts = collect_life_optimization_facts(context, payload)
    result = evaluate_life_optimization(facts)
    if result.state not in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        assert_valid(validate_life_optimization_result(result, context=context))
    return bind_life_optimization(context, result)
