"""P7-IMP-14 Narrative Composer: communicate Pack 07 truth, do not create it."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.diagnostics import (
    build_pack07_diagnostics,
    diagnostics_from_payload,
)
from engines.detailed_interpretation_engine.enums import DiagnosticStatus, EvaluationStatus
from engines.detailed_interpretation_engine.factories import build_canonical_analysis_context
from engines.detailed_interpretation_engine.narrative_composer.constants import FORBIDDEN_CUSTOMER_TOKENS
from engines.detailed_interpretation_engine.narrative_composer.engine import interpret_and_bind_narrative
from engines.detailed_interpretation_engine.narrative_composer.evaluate import evaluate_narrative
from engines.detailed_interpretation_engine.narrative_composer.facts import collect_narrative_facts
from engines.detailed_interpretation_engine.narrative_composer.labels import action_label
from engines.detailed_interpretation_engine.narrative_composer.presentation import present_narrative_customer
from engines.detailed_interpretation_engine.serialization import to_jsonable
from engines.detailed_interpretation_engine.validators import validate_narrative_result
from tests.detailed_interpretation.test_p7_imp_09_domains import CASE_0001
from tests.detailed_interpretation.test_p7_imp_11_luck_interaction import _natal_slice
from tests.detailed_interpretation.test_p7_imp_13_life_optimization import _bind_opt, _rehash, _temporal_payload


def _bind_nar(payload: dict[str, object]):
    context, bound = _bind_opt(payload)
    return interpret_and_bind_narrative(context, bound), bound


def _truth(context) -> object:
    runtime = context.runtime
    return to_jsonable(
        {
            "mc01": context.interpretation.mc01,
            "evidence_priority": runtime.interpretation.evidence_priority,
            "domains": _natal_slice(context),
            "luck_activation": runtime.temporal.luck_activation,
            "luck_interaction": runtime.temporal.luck_interaction,
            "temporal_activation": runtime.temporal.temporal_activation,
            "optimization": runtime.optimization,
            "ten_gods": runtime.interpretation.ten_gods.natal,
            "shen_sha": runtime.interpretation.shen_sha.individual,
        }
    )


def test_does_not_mutate_pattern_grade_domain_or_action() -> None:
    payload = _temporal_payload()
    before_ctx, bound = _bind_opt(payload)
    before = _truth(before_ctx)
    domains = before_ctx.runtime.domains
    optimization = before_ctx.runtime.optimization
    interpretation = before_ctx.runtime.interpretation
    mc01 = before_ctx.interpretation.mc01
    after_ctx = interpret_and_bind_narrative(before_ctx, bound)
    assert after_ctx.runtime.domains is domains
    assert after_ctx.runtime.optimization is optimization
    assert after_ctx.runtime.interpretation is interpretation
    assert after_ctx.interpretation.mc01 is mc01
    assert _truth(after_ctx) == before
    result = after_ctx.runtime.narrative.result
    assert result.status is EvaluationStatus.RESOLVED
    issues = validate_narrative_result(result, context=after_ctx)
    assert issues.status.value != "fail"


def test_executive_summary_comes_from_p0_p1_only() -> None:
    context, _ = _bind_nar(_temporal_payload())
    result = context.runtime.narrative.result
    findings = context.runtime.interpretation.evidence_priority.findings
    p0_p1 = [item.customer_label for item in findings if item.tier.value in {"P0", "P1"} and item.customer_label]
    later = [item.customer_label for item in findings if item.tier.value in {"P4", "P5"} and item.customer_label]
    assert result.executive_summary
    assert any(label and label in result.executive_summary for label in p0_p1)
    for label in later:
        if label and label not in " ".join(p0_p1):
            assert label not in result.executive_summary


def test_actions_match_optimization_top_three() -> None:
    context, _ = _bind_nar(_temporal_payload())
    result = context.runtime.narrative.result
    opt = context.runtime.optimization
    by_id = {item.action_id: item for item in opt.actions}
    expected = [
        action_label(by_id[action_id].recommended_action_key)
        for action_id in opt.top_priorities[:3]
        if action_id in by_id
    ]
    action_blocks = [item for item in result.blocks if item.block_type == "action"]
    titles = [item.title for item in action_blocks[:3]]
    assert titles == [item for item in expected if item]
    assert result.optimization
    for title in titles:
        assert title in result.optimization or title in result.closing_summary


def test_does_not_invent_facts_or_forbidden_copy() -> None:
    context, _ = _bind_nar(_temporal_payload())
    compact = present_narrative_customer(context.runtime.narrative.result)
    dump = str(compact).lower()
    assert compact.get("executive")
    assert compact.get("actions")
    assert "tr-p7-" not in dump
    assert "e-di-" not in dump
    for token in FORBIDDEN_CUSTOMER_TOKENS:
        assert token not in dump
    summaries = [
        item.summary
        for item in context.runtime.narrative.result.blocks
        if item.block_type in {"strength", "risk", "opportunity"} and item.summary
    ]
    assert summaries
    assert len(summaries) == len(set(summaries))


def test_graph_has_required_nodes_and_edges() -> None:
    context, _ = _bind_nar(_temporal_payload())
    graph = context.runtime.narrative.result.graph
    types = {item.node_type.value for item in graph.nodes}
    assert "executive_summary" in types
    assert "strength" in types or "risk" in types
    assert "action" in types
    assert "closing_summary" in types
    edge_types = {item.edge_type.value for item in graph.edges}
    assert edge_types <= {"supports", "explains", "qualifies", "contrasts", "expands", "summarizes"}
    assert graph.edges


def test_metamorphic_optimization_change_updates_narrative() -> None:
    context, bound = _bind_opt(_temporal_payload())
    original_ctx = interpret_and_bind_narrative(context, bound)
    original = original_ctx.runtime.narrative.result.optimization
    opt = context.runtime.optimization
    reversed_ids = tuple(reversed(opt.top_priorities))
    if reversed_ids == opt.top_priorities:
        return
    mutated = _rehash(replace(context, runtime=replace(context.runtime, optimization=replace(opt, top_priorities=reversed_ids))))
    after = interpret_and_bind_narrative(mutated, bound)
    assert after.runtime.optimization.top_priorities == reversed_ids
    assert after.runtime.narrative.result.optimization != original


def test_metamorphic_domain_change_updates_narrative() -> None:
    context, bound = _bind_opt(_temporal_payload())
    original_ctx = interpret_and_bind_narrative(context, bound)
    original = original_ctx.runtime.narrative.result.domains.get("wealth", "")
    wealth = context.runtime.domains.wealth
    mutated_natal = replace(wealth.natal, bottleneck="nút thắt kiểm chứng composer")
    mutated_domains = replace(context.runtime.domains, wealth=replace(wealth, natal=mutated_natal))
    mutated = _rehash(replace(context, runtime=replace(context.runtime, domains=mutated_domains)))
    after = interpret_and_bind_narrative(mutated, bound)
    assert after.runtime.domains.wealth.natal.bottleneck == "nút thắt kiểm chứng composer"
    assert after.runtime.narrative.result.domains.get("wealth", "") != original
    assert "nút thắt kiểm chứng composer" in after.runtime.narrative.result.domains.get("wealth", "")


def test_metamorphic_template_only_leaves_truth_unchanged(monkeypatch) -> None:
    context, bound = _bind_opt(_temporal_payload())
    before = _truth(context)
    facts = collect_narrative_facts(context, bound)
    monkeypatch.setattr(
        "engines.detailed_interpretation_engine.narrative_composer.evaluate.WHO_TEMPLATE",
        "Khác biệt {pattern} {grade}.",
    )
    rewritten = evaluate_narrative(facts)
    assert "Khác biệt" in rewritten.executive_summary
    assert _truth(context) == before
    after = interpret_and_bind_narrative(context, bound)
    assert after.runtime.optimization is context.runtime.optimization
    assert after.runtime.domains is context.runtime.domains


def test_empty_diagnostics_keep_narrative_not_evaluated() -> None:
    diagnostics = build_pack07_diagnostics(build_canonical_analysis_context("an-p7-nar-empty"))
    assert diagnostics.narrative is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.optimization is DiagnosticStatus.NOT_EVALUATED


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = _temporal_payload()
    snapshot = deepcopy(original)
    _bind_nar(original)
    assert original == snapshot


def test_live_case_0001_exposes_composer_without_hard_coded_copy() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    compact = body.get("detailed_narrative") or {}
    assert compact.get("executive")
    assert compact.get("strengths")
    assert compact.get("risks")
    assert compact.get("opportunities")
    assert compact.get("domains")
    assert len(compact["domains"]) == 6
    assert compact.get("luck")
    assert compact.get("actions")
    assert compact.get("closing")
    assert compact.get("title") == "LUẬN GIẢI TỔNG THỂ"
    dump = str(compact).lower()
    assert "tr-p7-" not in dump
    for token in FORBIDDEN_CUSTOMER_TOKENS:
        assert token not in dump
    assert body.get("narrative") != compact
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.narrative is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    data = live.json()["data"]
    assert data["narrative"] == "PASS"
    assert data["optimization"] == "PASS"
    assert data["domains"] == "PASS"
    assert data["contexts"] == "PASS"
    assert data["runtime_contract"] == "PASS"
    empty = client.get("/api/v1/dev/pack07/diagnostics")
    assert empty.status_code == 200
    assert empty.json()["data"]["narrative"] == "NOT_EVALUATED"
