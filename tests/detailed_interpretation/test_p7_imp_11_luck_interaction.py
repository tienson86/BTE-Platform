"""P7-IMP-11 Luck Interaction Engine: activation-to-activation, not natal rewrite."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.diagnostics import (
    build_pack07_diagnostics,
    diagnostics_from_payload,
)
from engines.detailed_interpretation_engine.enums import ActivationState, DiagnosticStatus
from engines.detailed_interpretation_engine.factories import build_canonical_analysis_context
from engines.detailed_interpretation_engine.luck_interaction.engine import (
    interpret_and_bind_luck_interaction,
)
from engines.detailed_interpretation_engine.luck_interaction.presentation import (
    present_luck_interaction_customer,
)
from engines.detailed_interpretation_engine.serialization import compute_content_hash, serialize_runtime_result, to_jsonable
from engines.detailed_interpretation_engine.validators import validate_luck_interaction_result
from tests.detailed_interpretation.test_p7_imp_09_domains import CASE_0001
from tests.detailed_interpretation.test_p7_imp_10_luck_activation import (
    MAIN,
    _bind_luck,
    _luck_payload,
    _natal_slice,
)

NATAL_DRIVER_IDS = {"hybrid", "mixed", "communication", "resilience"}


def _bind_interaction(payload: dict[str, object]):
    context, bound = _bind_luck(payload)
    return interpret_and_bind_luck_interaction(context), bound


def _immutable_slice(context) -> object:
    return to_jsonable(
        {
            "natal": _natal_slice(context),
            "luck_activation": context.runtime.temporal.luck_activation,
        }
    )


def _rehash(context):
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, metadata=cleared)
    hashed = replace(cleared, content_hash=compute_content_hash(serialize_runtime_result(runtime)))
    return replace(context, runtime=replace(runtime, metadata=hashed))


def _with_graph_edges(context, edges):
    graph = replace(context.runtime.domains.graph, edges=edges)
    domains = replace(context.runtime.domains, graph=graph)
    return _rehash(replace(context, runtime=replace(context.runtime, domains=domains)))


def _with_activation_item(context, domain_id: str, **changes):
    luck = context.runtime.temporal.luck_activation
    items = dict(luck.items)
    items[domain_id] = replace(items[domain_id], **changes)
    luck = replace(luck, items=items)
    temporal = replace(context.runtime.temporal, luck_activation=luck)
    return _rehash(replace(context, runtime=replace(context.runtime, temporal=temporal)))


def test_interaction_consumes_activation_without_recalculating() -> None:
    context, _ = _bind_interaction(_luck_payload())
    activation = context.runtime.temporal.luck_activation
    interaction = context.runtime.temporal.luck_interaction
    assert activation.status.value == "resolved"
    assert interaction.cycle_id == activation.cycle_id
    assert interaction.time_window == activation.time_window
    assert interaction.cycle_kind == "dai_van"
    issues = validate_luck_interaction_result(interaction, context=context)
    assert not issues.errors
    for finding in interaction.findings:
        assert finding.evidence_ids
        assert finding.source_domain in activation.items
        assert finding.target_domain in activation.items


def test_interaction_does_not_mutate_natal_or_luck_activation() -> None:
    payload = _luck_payload()
    before_ctx, bound = _bind_luck(payload)
    before = _immutable_slice(before_ctx)
    activation_obj = before_ctx.runtime.temporal.luck_activation
    after_ctx = interpret_and_bind_luck_interaction(before_ctx)
    assert _immutable_slice(after_ctx) == before
    assert after_ctx.runtime.temporal.luck_activation is activation_obj
    assert after_ctx.runtime.domains is before_ctx.runtime.domains


def test_authority_strong_is_not_career_support_without_natal_edge() -> None:
    context, _ = _bind_luck(_luck_payload())
    edges = tuple(
        edge
        for edge in context.runtime.domains.graph.edges
        if not (edge.source == "authority" and edge.target == "career" and edge.relation == "supports")
    )
    mutated = _with_graph_edges(context, edges)
    after = interpret_and_bind_luck_interaction(mutated)
    found = [
        item
        for item in after.runtime.temporal.luck_interaction.findings
        if item.source_domain == "authority"
        and item.target_domain == "career"
        and item.interaction_type == "support"
    ]
    assert found == []


def test_career_overload_is_not_automatic_vitality_stress() -> None:
    context, _ = _bind_luck(_luck_payload())
    edges = tuple(
        edge
        for edge in context.runtime.domains.graph.edges
        if not (edge.source == "vitality" and edge.target == "career")
    )
    mutated = _with_graph_edges(context, edges)
    after = interpret_and_bind_luck_interaction(mutated)
    found = [
        item
        for item in after.runtime.temporal.luck_interaction.findings
        if item.interaction_type in {"stress_transfer", "resource_shift"}
        and {item.source_domain, item.target_domain} == {"career", "vitality"}
    ]
    assert found == []


def test_wealth_active_is_not_automatic_relationship_conflict() -> None:
    context, _ = _bind_interaction(_luck_payload())
    found = [
        item
        for item in context.runtime.temporal.luck_interaction.findings
        if item.interaction_type in {"conflict", "trade_off"}
        and {item.source_domain, item.target_domain} == {"wealth", "relationship"}
    ]
    assert found == []
    natal_edges = [
        edge
        for edge in context.runtime.domains.graph.edges
        if {edge.source, edge.target} == {"wealth", "relationship"}
    ]
    assert natal_edges == []


def test_life_situation_is_not_a_new_natal_state() -> None:
    context, _ = _bind_interaction(_luck_payload())
    interaction = context.runtime.temporal.luck_interaction
    natal_states = {
        context.runtime.domains.authority.natal.state.value,
        context.runtime.domains.career.natal.state.value,
        context.runtime.domains.wealth.natal.state.value,
        context.runtime.domains.relationship.natal.state.value,
        context.runtime.domains.legacy.natal.state.value,
        context.runtime.domains.vitality.natal.state.value,
    }
    assert interaction.life_situation.temporality == "window_bound"
    assert interaction.life_situation.situation_id not in natal_states
    for domain_id in MAIN:
        natal = getattr(context.runtime.domains, domain_id).natal
        item = context.runtime.temporal.luck_activation.items[domain_id]
        assert natal.state.value == item.natal_state


def test_interaction_driver_is_not_domain_driver() -> None:
    context, _ = _bind_interaction(_luck_payload())
    interaction = context.runtime.temporal.luck_interaction
    assert interaction.interaction_driver not in NATAL_DRIVER_IDS
    for domain_id in MAIN:
        natal = getattr(context.runtime.domains, domain_id).natal
        assert interaction.interaction_driver != natal.driver_id


def test_interaction_bottleneck_does_not_rewrite_natal_bottleneck() -> None:
    payload = _luck_payload()
    before_ctx, bound = _bind_luck(payload)
    before_bottlenecks = {
        domain_id: getattr(before_ctx.runtime.domains, domain_id).natal.bottleneck
        for domain_id in MAIN
    }
    after_ctx = interpret_and_bind_luck_interaction(before_ctx)
    for domain_id in MAIN:
        natal = getattr(after_ctx.runtime.domains, domain_id).natal
        assert natal.bottleneck == before_bottlenecks[domain_id]
    bottleneck = after_ctx.runtime.temporal.luck_interaction.interaction_bottleneck
    assert bottleneck not in before_bottlenecks.values() or bottleneck in {"not_applicable", "none", ""}


def test_removing_one_activation_drops_dependent_edges() -> None:
    context, _ = _bind_luck(_luck_payload())
    before = interpret_and_bind_luck_interaction(context)
    dependent = [
        item.finding_id
        for item in before.runtime.temporal.luck_interaction.findings
        if "career" in {item.source_domain, item.target_domain}
    ]
    mutated = _with_activation_item(context, "career", activation_state=ActivationState.BLOCKED)
    after = interpret_and_bind_luck_interaction(mutated)
    remaining = {
        item.finding_id
        for item in after.runtime.temporal.luck_interaction.findings
        if "career" in {item.source_domain, item.target_domain}
    }
    assert remaining == set()
    assert not set(dependent) & remaining


def test_changing_one_activation_leaves_unrelated_pairs_unchanged() -> None:
    context, _ = _bind_luck(_luck_payload())
    before = interpret_and_bind_luck_interaction(context).runtime.temporal.luck_interaction
    unrelated_before = {
        (item.source_domain, item.target_domain, item.interaction_type)
        for item in before.findings
        if "authority" not in {item.source_domain, item.target_domain}
    }
    mutated = _with_activation_item(context, "authority", activation_state=ActivationState.DORMANT)
    after = interpret_and_bind_luck_interaction(mutated).runtime.temporal.luck_interaction
    unrelated_after = {
        (item.source_domain, item.target_domain, item.interaction_type)
        for item in after.findings
        if "authority" not in {item.source_domain, item.target_domain}
    }
    assert unrelated_before == unrelated_after


def test_removing_natal_support_edge_drops_support_interaction() -> None:
    context, _ = _bind_luck(_luck_payload())
    before = interpret_and_bind_luck_interaction(context)
    support_before = [
        item
        for item in before.runtime.temporal.luck_interaction.findings
        if item.source_domain == "authority"
        and item.target_domain == "career"
        and item.interaction_type == "support"
    ]
    edges = tuple(
        edge
        for edge in context.runtime.domains.graph.edges
        if not (edge.source == "authority" and edge.target == "career" and edge.relation == "supports")
    )
    after = interpret_and_bind_luck_interaction(_with_graph_edges(context, edges))
    support_after = [
        item
        for item in after.runtime.temporal.luck_interaction.findings
        if item.source_domain == "authority"
        and item.target_domain == "career"
        and item.interaction_type == "support"
    ]
    assert support_after == []
    if support_before:
        assert to_jsonable(after.runtime.temporal.luck_activation) == to_jsonable(
            context.runtime.temporal.luck_activation
        )


def test_graph_is_domain_to_domain_only() -> None:
    context, _ = _bind_interaction(_luck_payload())
    graph = context.runtime.temporal.luck_interaction.graph
    for edge in graph.edges:
        assert edge.source in context.runtime.temporal.luck_activation.items
        assert edge.target in context.runtime.temporal.luck_activation.items
        assert edge.evidence_ids
        assert not edge.source.startswith("dai_van")


def test_conflict_does_not_average_activations() -> None:
    before_ctx, _ = _bind_luck(_luck_payload())
    before_states = {
        domain_id: item.activation_state
        for domain_id, item in before_ctx.runtime.temporal.luck_activation.items.items()
    }
    after_ctx = interpret_and_bind_luck_interaction(before_ctx)
    after_states = {
        domain_id: item.activation_state
        for domain_id, item in after_ctx.runtime.temporal.luck_activation.items.items()
    }
    assert after_states == before_states
    conflicts = [
        item
        for item in after_ctx.runtime.temporal.luck_interaction.findings
        if item.interaction_type == "conflict"
    ]
    for finding in conflicts:
        assert after_states[finding.source_domain] is before_states[finding.source_domain]
        assert after_states[finding.target_domain] is before_states[finding.target_domain]


def test_empty_luck_keeps_interaction_not_applicable() -> None:
    from tests.detailed_interpretation.test_p7_imp_09_domains import _bind, _payload

    context, bound = _bind(_payload())
    context = interpret_and_bind_luck_interaction(context)
    assert context.runtime.temporal.luck_interaction.status.value == "not_applicable"
    assert present_luck_interaction_customer(context.runtime.temporal.luck_interaction) == {}


def test_empty_diagnostics_mark_interaction_not_implemented() -> None:
    diagnostics = build_pack07_diagnostics(build_canonical_analysis_context("an-p7-li-empty"))
    assert diagnostics.luck_interaction is DiagnosticStatus.NOT_IMPLEMENTED
    assert diagnostics.luck is DiagnosticStatus.NOT_IMPLEMENTED
    assert diagnostics.temporal is DiagnosticStatus.NOT_EVALUATED


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = _luck_payload()
    snapshot = deepcopy(original)
    _bind_interaction(original)
    assert original == snapshot


def test_live_case_0001_keeps_activation_and_exposes_interaction() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    luck = body.get("luck") or {}
    activation = luck.get("activation") or {}
    interaction = luck.get("interaction") or {}
    assert activation.get("items")
    assert interaction.get("title")
    dump = str(interaction)
    assert "TR-P7-" not in dump
    assert "E-DI-" not in dump
    assert "thăng chức" not in dump
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.domains is DiagnosticStatus.PASS
    assert diagnostics.luck is DiagnosticStatus.PASS
    assert diagnostics.luck_interaction is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    data = live.json()["data"]
    assert data["luck"] == "PASS"
    assert data["luck_interaction"] == "PASS"
    assert data["domains"] == "PASS"
    empty = client.get("/api/v1/dev/pack07/diagnostics")
    assert empty.status_code == 200
    assert empty.json()["data"]["luck_interaction"] == "NOT_IMPLEMENTED"
