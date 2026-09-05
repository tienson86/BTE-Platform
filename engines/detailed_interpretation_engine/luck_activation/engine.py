"""Luck Activation Engine. Projects current Đại Vận onto natal domains."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.luck_activation.constants import (
    ACTIVATION_CYCLE_KIND,
    LUCK_ACTIVATION_RULESET_VERSION,
    MAIN_ACTIVATION_IDS,
)
from engines.detailed_interpretation_engine.luck_activation.evaluate import (
    activation_order,
    dominant_activation_id,
    dominant_suppression_id,
    evaluate_domain_activations,
)
from engines.detailed_interpretation_engine.luck_activation.facts import collect_luck_activation_facts
from engines.detailed_interpretation_engine.luck_activation.graph import build_activation_graph
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.temporal import LuckActivationResult
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_luck_activation_result,
    validate_pack07_context,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def evaluate_luck_activation(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> LuckActivationResult:
    """Project the upstream Đại Vận onto natal domains. Does not rebuild luck identity."""
    facts = collect_luck_activation_facts(context, payload)
    if facts.cycle is None:
        return LuckActivationResult(
            analysis_id=facts.analysis_id or context.analysis_id,
            status=EvaluationStatus.NOT_APPLICABLE,
            cycle_kind=ACTIVATION_CYCLE_KIND,
            ruleset_version=LUCK_ACTIVATION_RULESET_VERSION,
        )
    items = evaluate_domain_activations(facts)
    order = activation_order(facts)
    graph = build_activation_graph(items, order, cycle_id=facts.cycle.cycle_id)
    evidence: list[str] = []
    traces: list[str] = []
    for domain_id in order:
        item = items[domain_id]
        evidence.extend(item.evidence_ids)
        traces.extend(item.trace_ids)
    stress = tuple(
        domain_id
        for domain_id in order
        if domain_id in MAIN_ACTIVATION_IDS
        and (
            items[domain_id].stress in {"high", "excessive"}
            or items[domain_id].activation_state.value in {"overloaded", "suppressed"}
        )
    )
    recovery = tuple(
        domain_id
        for domain_id in order
        if domain_id in MAIN_ACTIVATION_IDS and "recovery" in items[domain_id].activation_types
    )
    return LuckActivationResult(
        analysis_id=facts.analysis_id or context.analysis_id,
        status=EvaluationStatus.RESOLVED,
        cycle_kind=ACTIVATION_CYCLE_KIND,
        cycle_id=facts.cycle.cycle_id,
        luck_cycle_id=facts.cycle.cycle_id,
        time_window=facts.cycle.time_window,
        domain_activation_ids=order,
        order=order,
        items=items,
        graph=graph,
        dominant_activation=dominant_activation_id(items, order),
        dominant_suppression=dominant_suppression_id(items, order),
        stress_domains=tuple(dict.fromkeys(stress)),
        recovery_domains=tuple(dict.fromkeys(recovery)),
        evidence_ids=tuple(dict.fromkeys(evidence)),
        confidence=ConfidenceValue(value=0.72, summary="luck_activation"),
        trace_ids=tuple(dict.fromkeys(traces)),
        ruleset_version=LUCK_ACTIVATION_RULESET_VERSION,
        temporal_ten_god=facts.temporal_ten_god_label,
        temporal_stem=facts.cycle.stem,
        temporal_branch=facts.cycle.branch,
    )


def bind_luck_activation(
    context: CanonicalAnalysisContext,
    result: LuckActivationResult,
) -> CanonicalAnalysisContext:
    """Publish LuckActivationResult onto CanonicalRuntimeResult.temporal.luck_activation."""
    windows = dict(context.runtime.temporal.time_windows)
    if result.time_window:
        windows["luck_cycle"] = result.time_window
    section = replace(
        context.runtime.temporal,
        luck_activation=result,
        time_windows=windows,
        status=result.status,
    )
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, temporal=section, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    temporal_ctx = replace(
        context.temporal,
        status=result.status,
        luck=result,
        section=replace(context.temporal.section, luck_activation=result, time_windows=windows),
    )
    return replace(context, runtime=runtime, temporal=temporal_ctx)


def interpret_and_bind_luck_activation(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context, evaluate luck activation, bind the canonical result."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    result = evaluate_luck_activation(context, payload)
    if result.status not in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        assert_valid(validate_luck_activation_result(result, context=context))
    return bind_luck_activation(context, result)
