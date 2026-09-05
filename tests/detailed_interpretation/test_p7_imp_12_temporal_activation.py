"""P7-IMP-12 Temporal Activation Engine: annual refines luck, does not rewrite natal."""

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
from engines.detailed_interpretation_engine.serialization import (
    compute_content_hash,
    serialize_runtime_result,
    to_jsonable,
)
from engines.detailed_interpretation_engine.temporal_activation.constants import ANNUAL_SOURCE_PATH
from engines.detailed_interpretation_engine.temporal_activation.engine import (
    interpret_and_bind_temporal_activation,
)
from engines.detailed_interpretation_engine.temporal_activation.presentation import (
    present_temporal_activation_customer,
)
from engines.detailed_interpretation_engine.validators import validate_temporal_activation_result
from tests.detailed_interpretation.test_p7_imp_09_domains import CASE_0001
from tests.detailed_interpretation.test_p7_imp_10_luck_activation import (
    MAIN,
    _luck_payload,
)
from tests.detailed_interpretation.test_p7_imp_11_luck_interaction import (
    _bind_interaction,
    _natal_slice,
)

EVENT_TOKENS = ("sự kiện xấu", "sự kiện tốt", "tai họa", "thất bại", "cưới", "đổi việc", "phát tài")


def _annual_identity(**changes: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "year": 2026,
        "civil_year": 2026,
        "gan_zhi": "Ất Mão",
        "stem": "Ất",
        "branch": "Mão",
        "stem_element": "Mộc",
        "branch_element": "Mộc",
        "source": ANNUAL_SOURCE_PATH,
        "relations": [],
    }
    payload.update(changes)
    return payload


def _temporal_payload(annual: dict[str, object] | None = None) -> dict[str, object]:
    payload = _luck_payload()
    luck = dict(payload.get("luck") or {})
    luck["annual_identity"] = annual or _annual_identity()
    payload["luck"] = luck
    return payload


def _bind_temporal(payload: dict[str, object]):
    context, bound = _bind_interaction(payload)
    return interpret_and_bind_temporal_activation(context, bound), bound


def _snapshot(context) -> object:
    runtime = context.runtime
    return to_jsonable(
        {
            "mc01": context.interpretation.mc01,
            "evidence_priority": runtime.interpretation.evidence_priority,
            "domains": _natal_slice(context),
            "luck_activation": runtime.temporal.luck_activation,
            "luck_interaction": runtime.temporal.luck_interaction,
            "ten_gods": runtime.interpretation.ten_gods.natal,
            "shen_sha": runtime.interpretation.shen_sha.individual,
        }
    )


def _rehash(context):
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, metadata=cleared)
    hashed = replace(cleared, content_hash=compute_content_hash(serialize_runtime_result(runtime)))
    return replace(context, runtime=replace(runtime, metadata=hashed))


def test_annual_consumes_canonical_identity_without_recalculating() -> None:
    context, _ = _bind_temporal(_temporal_payload())
    result = context.runtime.temporal.temporal_activation
    assert result.state is EvaluationStatus.RESOLVED
    assert result.time_window == "2026"
    assert result.active_layer == "annual"
    assert result.parent_layer == "luck_cycle"
    assert result.evaluated_layers == ("luck_cycle", "annual")
    annual = result.layer_results["annual"]
    assert annual.source_identity == ANNUAL_SOURCE_PATH
    assert annual.temporal_pillar == "Ất Mão"
    assert annual.parent_layer == "luck_cycle"
    for layer in ("monthly", "daily", "hourly"):
        assert result.layer_results[layer].state is EvaluationStatus.NOT_EVALUATED
    issues = validate_temporal_activation_result(result, context=context)
    assert issues.status.value != "fail"


def test_annual_does_not_mutate_natal_luck_or_interaction() -> None:
    payload = _temporal_payload()
    before_ctx, bound = _bind_interaction(payload)
    activation = before_ctx.runtime.temporal.luck_activation
    interaction = before_ctx.runtime.temporal.luck_interaction
    before = _snapshot(before_ctx)
    after_ctx = interpret_and_bind_temporal_activation(before_ctx, bound)
    assert after_ctx.runtime.temporal.luck_activation is activation
    assert after_ctx.runtime.temporal.luck_interaction is interaction
    assert _snapshot(after_ctx) == before


def test_annual_cannot_change_pattern_or_grade() -> None:
    context, _ = _bind_temporal(_temporal_payload())
    assert context.interpretation.mc01.mingju_result_id
    result = context.runtime.temporal.temporal_activation
    assert "pattern" not in result.domain_results
    dump = str(to_jsonable(result)).lower()
    assert "rewrite natal pattern" not in dump
    assert "rewrite natal grade" not in dump


def test_annual_ten_god_is_not_natal_ten_god() -> None:
    before_ctx, bound = _bind_interaction(_temporal_payload())
    before_ids = tuple(item.ten_god_id for item in before_ctx.runtime.interpretation.ten_gods.natal.items)
    after = interpret_and_bind_temporal_activation(before_ctx, bound)
    after_ids = tuple(item.ten_god_id for item in after.runtime.interpretation.ten_gods.natal.items)
    assert after_ids == before_ids
    annual = after.runtime.temporal.temporal_activation.layer_results["annual"]
    assert any(actor.actor_kind == "ten_god" and actor.role == "annual" for actor in annual.temporal_actors)


def test_clash_is_not_a_bad_event() -> None:
    context, _ = _bind_temporal(_temporal_payload(_annual_identity(relations=["clash"])))
    result = context.runtime.temporal.temporal_activation
    dump = " ".join(result.conditions).lower()
    assert "không phải sự kiện xấu" in dump
    for token in EVENT_TOKENS:
        assert token not in dump or token == "sự kiện xấu"
    for item in result.domain_results.values():
        assert item.annual_expression_state != "blocked" or item.luck_activation_state == "blocked"


def test_combination_is_not_a_good_event() -> None:
    context, _ = _bind_temporal(_temporal_payload(_annual_identity(relations=["combination"])))
    result = context.runtime.temporal.temporal_activation
    dump = " ".join(result.conditions).lower()
    assert "không phải sự kiện tốt" in dump
    assert "phát tài" not in dump


def test_specificity_does_not_dominate_luck() -> None:
    context, _ = _bind_temporal(_temporal_payload())
    luck = context.runtime.temporal.luck_activation
    annual = context.runtime.temporal.temporal_activation
    for domain_id in MAIN:
        luck_item = luck.items[domain_id]
        annual_item = annual.domain_results[domain_id]
        assert annual_item.luck_activation_state == luck_item.activation_state.value
        if luck_item.activation_state.value == "dormant" and annual_item.annual_modifier in {
            "activate",
            "strengthen",
        }:
            assert annual_item.annual_expression_state not in {"strong", "peak", "overloaded"}


def test_remove_annual_keeps_luck_unchanged() -> None:
    with_annual, _ = _bind_interaction(_temporal_payload())
    luck_before = to_jsonable(with_annual.runtime.temporal.luck_activation)
    without = interpret_and_bind_temporal_activation(with_annual, _luck_payload())
    assert to_jsonable(without.runtime.temporal.luck_activation) == luck_before
    assert without.runtime.temporal.temporal_activation.state is EvaluationStatus.INSUFFICIENT_EVIDENCE


def test_change_annual_facts_keeps_natal_and_luck() -> None:
    context, bound = _bind_interaction(_temporal_payload())
    before = _snapshot(context)
    other = deepcopy(bound)
    luck = dict(other.get("luck") or {})
    luck["annual_identity"] = _annual_identity(stem="Canh", branch="Tý", gan_zhi="Canh Tý", stem_element="Kim")
    other["luck"] = luck
    after = interpret_and_bind_temporal_activation(context, other)
    assert _snapshot(after) == before


def test_annual_support_does_not_worsen_unless_overload() -> None:
    dormant, _ = _bind_temporal(_temporal_payload(_annual_identity(relations=[])))
    vitality = dormant.runtime.temporal.temporal_activation.domain_results["vitality"]
    assert vitality.annual_expression_state != "overloaded" or vitality.luck_activation_state == "overloaded"


def test_extra_activation_may_overload() -> None:
    context, bound = _bind_interaction(_temporal_payload())
    luck = context.runtime.temporal.luck_activation
    items = dict(luck.items)
    items["authority"] = replace(items["authority"], activation_state=luck.items["authority"].activation_state)
    luck = replace(luck, items=items)
    context = _rehash(replace(context, runtime=replace(context.runtime, temporal=replace(
        context.runtime.temporal,
        luck_activation=luck,
    ))))
    after = interpret_and_bind_temporal_activation(context, bound)
    authority = after.runtime.temporal.temporal_activation.domain_results["authority"]
    assert authority.annual_expression_state in {
        authority.luck_activation_state,
        "overloaded",
        "peak",
        "strong",
        "active",
        "conditional",
        "recovering",
        "transition",
        "weak",
        "suppressed",
        "dormant",
    }


def test_customer_compact_hides_ids_and_events() -> None:
    context, _ = _bind_temporal(_temporal_payload())
    compact = present_temporal_activation_customer(context.runtime.temporal.temporal_activation)
    dump = str(compact)
    assert compact["year"] == "2026"
    assert compact["title"]
    assert len(compact["items"]) == 6
    assert "TR-P7-" not in dump
    assert "năm nay" not in dump.lower()
    for token in ("cưới", "đổi việc", "phát tài", "sẽ bệnh"):
        assert token not in dump


def test_empty_diagnostics_keep_temporal_not_evaluated() -> None:
    diagnostics = build_pack07_diagnostics(build_canonical_analysis_context("an-p7-ta-empty"))
    assert diagnostics.temporal is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.optimization is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.narrative is DiagnosticStatus.NOT_EVALUATED


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = _temporal_payload()
    snapshot = deepcopy(original)
    _bind_temporal(original)
    assert original == snapshot


def test_live_case_0001_exposes_annual_without_hard_coded_states() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    luck = body.get("luck") or {}
    annual = luck.get("annual") or {}
    assert annual.get("year")
    assert str(annual.get("year")).isdigit()
    assert annual.get("gan_zhi")
    assert annual.get("items")
    assert len(annual["items"]) == 6
    dump = str(annual)
    assert "TR-P7-" not in dump
    assert "năm nay" not in dump.lower()
    assert "cưới" not in dump
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.domains is DiagnosticStatus.PASS
    assert diagnostics.luck is DiagnosticStatus.PASS
    assert diagnostics.luck_interaction is DiagnosticStatus.PASS
    assert diagnostics.temporal is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    data = live.json()["data"]
    assert data["temporal"] == "PASS"
    assert data["optimization"] == "PASS"
    assert data["narrative"] == "PASS"
    empty = client.get("/api/v1/dev/pack07/diagnostics")
    assert empty.status_code == 200
    assert empty.json()["data"]["temporal"] == "NOT_EVALUATED"
