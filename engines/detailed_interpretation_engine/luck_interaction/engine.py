"""Luck Interaction Engine. Projects activation-to-activation pressure. Does not rewrite activation."""

from __future__ import annotations

from dataclasses import replace

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.luck_interaction.constants import (
    INTERACTION_CYCLE_KIND,
    LUCK_INTERACTION_RULESET_VERSION,
)
from engines.detailed_interpretation_engine.luck_interaction.evaluate import (
    build_life_situation,
    build_priority,
    elect_interaction_bottleneck,
    elect_interaction_driver,
    evaluate_findings,
    highest_opportunity_text,
    highest_risk_text,
)
from engines.detailed_interpretation_engine.luck_interaction.facts import collect_luck_interaction_facts
from engines.detailed_interpretation_engine.luck_interaction.graph import build_interaction_graph
from engines.detailed_interpretation_engine.luck_interaction.models import (
    LifeSituationResult,
    ResourceShift,
    StressTransfer,
)
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.temporal import LuckInteractionResult
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_luck_interaction_result,
    validate_pack07_context,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def evaluate_luck_interaction(context: CanonicalAnalysisContext) -> LuckInteractionResult:
    """Derive window interactions from natal DomainGraph plus current Luck Activation."""
    facts = collect_luck_interaction_facts(context)
    activation = facts.activation
    if activation.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return LuckInteractionResult(
            analysis_id=facts.analysis_id or context.analysis_id,
            status=EvaluationStatus.NOT_APPLICABLE,
            cycle_kind=INTERACTION_CYCLE_KIND,
            cycle_id=activation.cycle_id,
            time_window=activation.time_window,
            ruleset_version=LUCK_INTERACTION_RULESET_VERSION,
            interaction_driver="not_applicable",
            interaction_bottleneck="not_applicable",
            life_situation=LifeSituationResult(
                situation_id="not_applicable",
                situation_state="not_applicable",
                temporality="window_bound",
            ),
        )
    findings = evaluate_findings(facts)
    priority = build_priority(findings)
    driver = elect_interaction_driver(findings)
    bottleneck = elect_interaction_bottleneck(findings)
    situation = build_life_situation(activation, findings, driver, bottleneck)
    graph = build_interaction_graph(activation.items, findings, activation.order)
    evidence: list[str] = []
    traces: list[str] = []
    conditions: list[str] = []
    shifts: list[ResourceShift] = []
    transfers: list[StressTransfer] = []
    for finding in findings:
        evidence.extend(finding.evidence_ids)
        traces.extend(finding.trace_ids)
        conditions.extend(finding.conditions)
        if finding.resource_shift is not None:
            shifts.append(finding.resource_shift)
        if finding.stress_transfer is not None:
            transfers.append(finding.stress_transfer)
    traces.append("TR-P7-LI-window")
    ids = tuple(item.finding_id for item in findings)
    return LuckInteractionResult(
        analysis_id=facts.analysis_id or context.analysis_id,
        status=EvaluationStatus.RESOLVED,
        cycle_kind=INTERACTION_CYCLE_KIND,
        cycle_id=activation.cycle_id,
        time_window=activation.time_window,
        ruleset_version=LUCK_INTERACTION_RULESET_VERSION,
        findings=findings,
        finding_ids=ids,
        graph=graph,
        priority=priority,
        life_situation=situation,
        interaction_driver=driver,
        interaction_bottleneck=bottleneck,
        opportunity=highest_opportunity_text(findings),
        risk=highest_risk_text(findings),
        conditions=tuple(dict.fromkeys(conditions)),
        evidence_ids=tuple(dict.fromkeys(evidence)),
        confidence=ConfidenceValue(value=0.7, summary="luck_interaction"),
        warnings=(),
        trace=tuple(dict.fromkeys(traces)),
        trace_ids=tuple(dict.fromkeys(traces)),
        resource_shifts=tuple(shifts),
        stress_transfers=tuple(transfers),
    )


def bind_luck_interaction(
    context: CanonicalAnalysisContext,
    result: LuckInteractionResult,
) -> CanonicalAnalysisContext:
    """Publish LuckInteractionResult onto CanonicalRuntimeResult.temporal.luck_interaction."""
    activation = context.runtime.temporal.luck_activation
    section = replace(context.runtime.temporal, luck_interaction=result)
    if section.luck_activation is not activation:
        section = replace(section, luck_activation=activation)
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, temporal=section, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    temporal_ctx = replace(
        context.temporal,
        interaction=result,
        section=replace(context.temporal.section, luck_interaction=result, luck_activation=activation),
    )
    return replace(context, runtime=runtime, temporal=temporal_ctx)


def interpret_and_bind_luck_interaction(context: CanonicalAnalysisContext) -> CanonicalAnalysisContext:
    """Validate context, evaluate luck interaction, bind without recalculating activation."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    result = evaluate_luck_interaction(context)
    if result.status not in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        assert_valid(validate_luck_interaction_result(result, context=context))
    return bind_luck_interaction(context, result)
