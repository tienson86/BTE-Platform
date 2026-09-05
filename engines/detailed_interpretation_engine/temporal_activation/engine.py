"""Temporal Activation Engine. Annual refines luck envelope. Does not rewrite natal or luck."""

from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from engines.detailed_interpretation_engine.context_layers import CanonicalAnalysisContext
from engines.detailed_interpretation_engine.enums import EvaluationStatus
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result
from engines.detailed_interpretation_engine.temporal import TemporalActivationResult
from engines.detailed_interpretation_engine.temporal_activation.constants import (
    ANNUAL_SOURCE_PATH,
    CONTRACT_SHELL_LAYERS,
    PARENT_OF,
    REQUESTED_RUNTIME_LAYERS,
    TEMPORAL_ACTIVATION_RULESET_VERSION,
)
from engines.detailed_interpretation_engine.temporal_activation.evaluate import (
    dominant_annual_activation,
    dominant_annual_suppression,
    evaluate_annual_domains,
    layer_modifiers,
    luck_layer_domains,
    temporal_salience,
)
from engines.detailed_interpretation_engine.temporal_activation.facts import collect_temporal_activation_facts
from engines.detailed_interpretation_engine.temporal_activation.models import (
    TemporalActor,
    TemporalLayerResult,
)
from engines.detailed_interpretation_engine.validators import (
    assert_valid,
    validate_pack07_context,
    validate_temporal_activation_result,
)
from engines.detailed_interpretation_engine.value_objects import ConfidenceValue


def evaluate_temporal_activation(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> TemporalActivationResult:
    """Evaluate current luck-cycle plus annual layers only. Lazy: no month/day/hour grid."""
    facts = collect_temporal_activation_facts(context, payload)
    luck = facts.luck_cycle_result
    if luck.status in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        return _unevaluated(facts.analysis_id or context.analysis_id, EvaluationStatus.NOT_APPLICABLE)
    luck_layer = _luck_cycle_layer(luck)
    layers: dict[str, TemporalLayerResult] = {
        "luck_cycle": luck_layer,
        **{layer: _shell(layer) for layer in CONTRACT_SHELL_LAYERS},
    }
    if facts.annual is None:
        layers["annual"] = _shell("annual")
        return TemporalActivationResult(
            analysis_id=facts.analysis_id or context.analysis_id,
            state=EvaluationStatus.INSUFFICIENT_EVIDENCE,
            requested_layers=REQUESTED_RUNTIME_LAYERS,
            evaluated_layers=("luck_cycle",),
            time_window=luck.time_window,
            active_layer="luck_cycle",
            parent_layer="natal",
            layer_results=layers,
            ruleset_version=TEMPORAL_ACTIVATION_RULESET_VERSION,
            warnings=("annual_identity_missing",),
        )
    items = evaluate_annual_domains(facts)
    order = tuple(items)
    annual = facts.annual
    year = annual.civil_year or annual.year
    actors = _annual_actors(facts)
    annual_layer = TemporalLayerResult(
        layer="annual",
        time_window=year,
        parent_layer="luck_cycle",
        temporal_pillar=annual.gan_zhi,
        temporal_actors=actors,
        modifiers=layer_modifiers(items),
        domain_activation=items,
        confidence=ConfidenceValue(value=0.68, summary="temporal_activation"),
        evidence_ids=tuple(dict.fromkeys(item for row in items.values() for item in row.evidence_ids)),
        trace_ids=tuple(dict.fromkeys(item for row in items.values() for item in row.trace_ids)),
        state=EvaluationStatus.RESOLVED,
        source_identity=annual.source_identity or ANNUAL_SOURCE_PATH,
    )
    layers["annual"] = annual_layer
    stress = tuple(
        domain_id
        for domain_id in order
        if items[domain_id].stress in {"high", "excessive"}
        or items[domain_id].annual_expression_state in {"overloaded", "suppressed"}
    )
    recovery = tuple(
        domain_id
        for domain_id in order
        if items[domain_id].recovery != "none" or items[domain_id].annual_expression_state == "recovering"
    )
    bottlenecks = tuple(
        dict.fromkeys(
            items[domain_id].temporal_bottleneck
            for domain_id in order
            if items[domain_id].temporal_bottleneck not in {"", "none", "not_applicable"}
        )
    )
    return TemporalActivationResult(
        analysis_id=facts.analysis_id or context.analysis_id,
        state=EvaluationStatus.RESOLVED,
        requested_layers=REQUESTED_RUNTIME_LAYERS,
        evaluated_layers=REQUESTED_RUNTIME_LAYERS,
        time_window=year,
        active_layer="annual",
        parent_layer="luck_cycle",
        layer_results=layers,
        domain_results=items,
        temporal_salience=temporal_salience(facts, items),
        dominant_activation=dominant_annual_activation(items, order),
        dominant_suppression=dominant_annual_suppression(items, order),
        bottlenecks=bottlenecks,
        stress=tuple(dict.fromkeys(stress)),
        recovery=tuple(dict.fromkeys(recovery)),
        conditions=tuple(dict.fromkeys(item for row in items.values() for item in row.conditions)),
        warnings=("not_an_event_prediction", "specificity_is_not_dominance"),
        confidence=ConfidenceValue(value=0.68, summary="temporal_activation"),
        evidence_ids=annual_layer.evidence_ids,
        trace_ids=annual_layer.trace_ids + ("TR-P7-TA-window",),
        ruleset_version=TEMPORAL_ACTIVATION_RULESET_VERSION,
    )


def bind_temporal_activation(
    context: CanonicalAnalysisContext,
    result: TemporalActivationResult,
) -> CanonicalAnalysisContext:
    """Publish TemporalActivationResult without replacing luck activation or interaction."""
    activation = context.runtime.temporal.luck_activation
    interaction = context.runtime.temporal.luck_interaction
    windows = dict(context.runtime.temporal.time_windows)
    if activation.time_window:
        windows["luck_cycle"] = activation.time_window
    if result.time_window:
        windows["annual"] = result.time_window
    section = replace(
        context.runtime.temporal,
        luck_activation=activation,
        luck_interaction=interaction,
        temporal_activation=result,
        time_windows=windows,
        requested_layers=result.requested_layers or context.runtime.temporal.requested_layers,
    )
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, temporal=section, metadata=cleared)
    serialized = serialize_runtime_result(runtime)
    metadata = replace(cleared, content_hash=compute_content_hash(serialized))
    runtime = replace(runtime, metadata=metadata)
    temporal_ctx = replace(
        context.temporal,
        temporal=result,
        luck=activation,
        interaction=interaction,
        section=replace(
            context.temporal.section,
            luck_activation=activation,
            luck_interaction=interaction,
            temporal_activation=result,
            time_windows=windows,
        ),
    )
    return replace(context, runtime=runtime, temporal=temporal_ctx)


def interpret_and_bind_temporal_activation(
    context: CanonicalAnalysisContext,
    payload: Mapping[str, Any] | None,
) -> CanonicalAnalysisContext:
    """Validate context, evaluate annual temporal activation, bind without mutating luck."""
    if context.analysis_id.strip():
        assert_valid(validate_pack07_context(context))
    result = evaluate_temporal_activation(context, payload)
    if result.state not in {EvaluationStatus.NOT_EVALUATED, EvaluationStatus.NOT_APPLICABLE}:
        assert_valid(validate_temporal_activation_result(result, context=context))
    return bind_temporal_activation(context, result)


def _unevaluated(analysis_id: str, state: EvaluationStatus) -> TemporalActivationResult:
    return TemporalActivationResult(
        analysis_id=analysis_id,
        state=state,
        requested_layers=REQUESTED_RUNTIME_LAYERS,
        evaluated_layers=(),
        layer_results={layer: _shell(layer) for layer in ("luck_cycle", "annual") + CONTRACT_SHELL_LAYERS},
        ruleset_version=TEMPORAL_ACTIVATION_RULESET_VERSION,
    )


def _shell(layer: str) -> TemporalLayerResult:
    return TemporalLayerResult(
        layer=layer,
        parent_layer=PARENT_OF.get(layer, ""),
        state=EvaluationStatus.NOT_EVALUATED,
    )


def _luck_cycle_layer(luck: Any) -> TemporalLayerResult:
    pillar = f"{luck.temporal_stem} {luck.temporal_branch}".strip()
    actors: tuple[TemporalActor, ...] = ()
    if luck.temporal_ten_god:
        actors = (
            TemporalActor(
                actor_kind="ten_god",
                actor_id="luck_cycle",
                label=luck.temporal_ten_god,
                role="luck_cycle",
            ),
        )
    return TemporalLayerResult(
        layer="luck_cycle",
        time_window=luck.time_window,
        parent_layer="natal",
        temporal_pillar=pillar,
        temporal_actors=actors,
        domain_activation=luck_layer_domains(luck),
        confidence=luck.confidence,
        evidence_ids=luck.evidence_ids,
        trace_ids=("TR-P7-TA-luck-cycle",),
        state=luck.status,
        source_identity="engines.luck_engine.engine.LuckEngine",
    )


def _annual_actors(facts: Any) -> tuple[TemporalActor, ...]:
    annual = facts.annual
    actors = [
        TemporalActor(
            actor_kind="ten_god",
            actor_id=annual.god_id or "annual_ten_god",
            label=annual.ten_god_label,
            role="annual",
        )
    ]
    if annual.stem_element:
        actors.append(
            TemporalActor(
                actor_kind="five_element",
                actor_id=annual.stem_element,
                label=annual.stem_element,
                role="annual",
                action=facts.element_action,
            )
        )
    if annual.branch_element and annual.branch_element != annual.stem_element:
        actors.append(
            TemporalActor(
                actor_kind="five_element",
                actor_id=annual.branch_element,
                label=annual.branch_element,
                role="annual",
                action=facts.element_action,
            )
        )
    return tuple(actors)
