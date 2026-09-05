"""Ten Gods natal interpretation engine. Deterministic; no LLM."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.constants import SCHEMA_TEN_GODS
from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.evidence import InterpretationSection, TenGodEcosystem
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.ten_gods.combinations.engine import interpret_ten_god_combinations
from engines.detailed_interpretation_engine.ten_gods.combinations.models import TenGodCombinationCollection
from engines.detailed_interpretation_engine.ten_gods.constants import CANONICAL_TEN_GOD_IDS
from engines.detailed_interpretation_engine.ten_gods.ecosystem.engine import interpret_ten_gods_ecosystem
from engines.detailed_interpretation_engine.ten_gods.ecosystem.models import TenGodEcosystemResult
from engines.detailed_interpretation_engine.ten_gods.evaluate import evaluate_ten_god
from engines.detailed_interpretation_engine.ten_gods.facts import extract_ten_god_facts, has_ten_gods_facts
from engines.detailed_interpretation_engine.ten_gods.models import TenGodInterpretationCollection
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue, TraceRef
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_pack07_context,
    validate_ten_god_combinations,
    validate_ten_god_ecosystem,
    validate_ten_gods_collection,
)


def interpret_ten_gods(
    payload: Mapping[str, Any] | None,
    *,
    analysis_id: str = "",
) -> TenGodInterpretationCollection:
    """Evaluate all 10 canonical Ten Gods from upstream facts."""
    facts = extract_ten_god_facts(payload)
    items = tuple(evaluate_ten_god(god_id, facts) for god_id in CANONICAL_TEN_GOD_IDS)
    evidence_ids = tuple(item.evidence_ids[0] for item in items if item.evidence_ids)
    trace_ids = tuple(trace for item in items for trace in item.trace_ids)
    summary: tuple[str, ...]
    if not facts.available:
        state = EvaluationStatus.UNRESOLVED
        summary = ("source:unavailable",)
        confidence = ConfidenceValue(summary="unresolved")
    elif not facts.mc01_bound:
        state = EvaluationStatus.PARTIALLY_RESOLVED
        summary = ("source:ten_gods_engine", "mc01:not_bound")
        confidence = ConfidenceValue(summary="low")
    else:
        state = EvaluationStatus.RESOLVED
        summary = ("source:ten_gods_engine", "mc01:bound")
        confidence = ConfidenceValue(summary="moderate")
    return TenGodInterpretationCollection(
        analysis_id=analysis_id,
        state=state,
        items=items,
        summary=summary,
        evidence_ids=evidence_ids,
        trace_ids=trace_ids,
        confidence=confidence,
    )


def bind_ten_gods_collection(
    context: CanonicalAnalysisContext,
    collection: TenGodInterpretationCollection,
    combinations: TenGodCombinationCollection | None = None,
    ecosystem: TenGodEcosystemResult | None = None,
) -> CanonicalAnalysisContext:
    """Publish natal, combinations, and ecosystem onto interpretation.ten_gods."""
    combo = combinations or TenGodCombinationCollection(analysis_id=collection.analysis_id)
    eco = ecosystem or TenGodEcosystemResult(analysis_id=collection.analysis_id)
    finding_ids = tuple(item.ten_god_id for item in collection.items) + tuple(
        item.combination_id for item in combo.items if item.combination_id
    )
    traces = collection.trace_ids + combo.trace_ids + eco.trace_ids
    evidence = collection.evidence_ids + combo.evidence_ids + eco.evidence_ids
    shell = TenGodEcosystem(
        schema_version=SCHEMA_TEN_GODS,
        status=collection.state,
        finding_ids=finding_ids,
        trace=TraceRef(trace_ids=traces, evidence_ids=evidence),
        natal=collection,
        combinations=combo,
        ecosystem=eco,
    )
    section = InterpretationSection(
        ten_gods=shell,
        shen_sha=context.runtime.interpretation.shen_sha,
        evidence_priority=context.runtime.interpretation.evidence_priority,
        status=collection.state,
        confidence=collection.confidence,
        trace_ids=traces,
    )
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, interpretation=section, metadata=cleared)
    payload = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(payload))
    runtime = replace(runtime, metadata=metadata)
    return replace(context, runtime=runtime, status=collection.state)


def interpret_and_bind_ten_gods(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context when identity exists, evaluate Ten Gods layers, bind result."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    if not has_ten_gods_facts(payload):
        return context
    facts = extract_ten_god_facts(payload)
    collection = interpret_ten_gods(payload, analysis_id=context.analysis_id)
    assert_valid(validate_ten_gods_collection(collection))
    combinations = interpret_ten_god_combinations(collection, mc01_bound=facts.mc01_bound)
    assert_valid(validate_ten_god_combinations(combinations, natal=collection))
    ecosystem = interpret_ten_gods_ecosystem(
        collection, combinations, mc01_bound=facts.mc01_bound
    )
    assert_valid(validate_ten_god_ecosystem(ecosystem, natal=collection, combinations=combinations))
    return bind_ten_gods_collection(context, collection, combinations, ecosystem)
