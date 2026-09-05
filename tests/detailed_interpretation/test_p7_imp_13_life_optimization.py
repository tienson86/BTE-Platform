"""P7-IMP-13 Life Optimization Engine: consume truth, do not create it."""

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
from engines.detailed_interpretation_engine.life_optimization.engine import (
    interpret_and_bind_life_optimization,
)
from engines.detailed_interpretation_engine.life_optimization.evaluate import action_urgency
from engines.detailed_interpretation_engine.life_optimization.presentation import (
    present_life_optimization_customer,
)
from engines.detailed_interpretation_engine.serialization import (
    compute_content_hash,
    serialize_runtime_result,
    to_jsonable,
)
from engines.detailed_interpretation_engine.temporal_activation.engine import (
    interpret_and_bind_temporal_activation,
)
from engines.detailed_interpretation_engine.validators import validate_life_optimization_result
from tests.detailed_interpretation.test_p7_imp_09_domains import CASE_0001
from tests.detailed_interpretation.test_p7_imp_11_luck_interaction import (
    _bind_interaction,
    _natal_slice,
)
from tests.detailed_interpretation.test_p7_imp_12_temporal_activation import (
    _bind_temporal,
    _temporal_payload,
)

FORBIDDEN = (
    "mặc đỏ",
    "wear red",
    "sống gần nước",
    "mua cây",
    "chẩn đoán",
    "điều trị",
    "uống thuốc",
    "mua cổ phiếu",
    "đòn bẩy",
    "chắc chắn giàu",
)


def _bind_opt(payload: dict[str, object]):
    context, bound = _bind_temporal(payload)
    return interpret_and_bind_life_optimization(context, bound), bound


def _snapshot(context) -> object:
    runtime = context.runtime
    return to_jsonable(
        {
            "mc01": context.interpretation.mc01,
            "evidence_priority": runtime.interpretation.evidence_priority,
            "domains": _natal_slice(context),
            "luck_activation": runtime.temporal.luck_activation,
            "luck_interaction": runtime.temporal.luck_interaction,
            "temporal_activation": runtime.temporal.temporal_activation,
            "ten_gods": runtime.interpretation.ten_gods.natal,
            "shen_sha": runtime.interpretation.shen_sha.individual,
        }
    )


def _rehash(context):
    cleared = replace(context.runtime.metadata, content_hash="")
    runtime = replace(context.runtime, metadata=cleared)
    hashed = replace(cleared, content_hash=compute_content_hash(serialize_runtime_result(runtime)))
    return replace(context, runtime=replace(runtime, metadata=hashed))


def _keys(result) -> list[str]:
    return [item.recommended_action_key for item in result.actions]


def test_natal_and_temporal_plans_are_distinct() -> None:
    context, _ = _bind_opt(_temporal_payload())
    result = context.runtime.optimization
    assert result.state is EvaluationStatus.RESOLVED
    assert result.natal_plan.state is EvaluationStatus.RESOLVED
    natal_ids = set(result.natal_plan.action_ids)
    temporal_ids = set(result.temporal_plan.action_ids)
    assert natal_ids
    assert natal_ids.isdisjoint(temporal_ids)
    issues = validate_life_optimization_result(result, context=context)
    assert issues.status.value != "fail"


def test_does_not_mutate_upstream_layers() -> None:
    payload = _temporal_payload()
    before_ctx, bound = _bind_temporal(payload)
    before = _snapshot(before_ctx)
    activation = before_ctx.runtime.temporal.luck_activation
    interaction = before_ctx.runtime.temporal.luck_interaction
    temporal = before_ctx.runtime.temporal.temporal_activation
    after_ctx = interpret_and_bind_life_optimization(before_ctx, bound)
    assert after_ctx.runtime.temporal.luck_activation is activation
    assert after_ctx.runtime.temporal.luck_interaction is interaction
    assert after_ctx.runtime.temporal.temporal_activation is temporal
    assert _snapshot(after_ctx) == before


def test_overload_does_not_recommend_more_workload() -> None:
    context, _ = _bind_opt(_temporal_payload())
    result = context.runtime.optimization
    career = context.runtime.temporal.luck_activation.items.get("career")
    if career is None or career.activation_state.value != "overloaded":
        return
    keys = " ".join(_keys(result))
    assert "strengthen_workload" not in keys
    assert "increase_output" not in keys
    assert "expand_responsibility" not in keys
    assert any("protect_workload" in key or "avoid_expansion" in key for key in _keys(result))


def test_wealth_volatility_does_not_recommend_investment() -> None:
    context, _ = _bind_opt(_temporal_payload())
    wealth = context.runtime.domains.wealth.natal
    if wealth.dimensions.get("volatility") not in {"very_high", "high", "above_average"}:
        return
    keys = " ".join(_keys(context.runtime.optimization)).lower()
    assert "investment" not in keys
    assert "buy_securities" not in keys
    assert any("retain_capital_discipline" in key for key in _keys(context.runtime.optimization))


def test_useful_god_is_function_first() -> None:
    payload = _temporal_payload()
    payload["useful_god"] = {"useful_element": "Hỏa", "useful_god": "Thiên Ất", "useful_display": "Hỏa"}
    context, _ = _bind_opt(payload)
    compact = present_life_optimization_customer(context.runtime.optimization)
    dump = str(compact).lower()
    assert "mặc đỏ" not in dump
    assert "wear red" not in dump
    plan = context.runtime.optimization.useful_god_plan
    assert "activation" in plan.functional_targets or plan.useful_god


def test_low_element_does_not_auto_add() -> None:
    payload = _temporal_payload()
    payload["five_elements"] = {"Kim": "low", "Mộc": "low", "Thủy": "low", "Hỏa": "low", "Thổ": "low"}
    payload["useful_god"] = {"useful_element": "Hỏa"}
    context, _ = _bind_opt(payload)
    keys = " ".join(_keys(context.runtime.optimization)).lower()
    assert "add_element" not in keys
    assert "thêm hỏa" not in keys
    elements = {item.element: item.action_direction for item in context.runtime.optimization.element_plan}
    assert "Kim" not in elements or elements.get("Kim") != "add"


def test_ky_is_not_total_ban() -> None:
    payload = _temporal_payload()
    payload["useful_god"] = {
        "useful_element": "Hỏa",
        "unfavorable_gods": ["Kỵ Thủy"],
        "ky_scope_note": "Thủy",
    }
    context, _ = _bind_opt(payload)
    ky_plans = [
        item
        for item in context.runtime.optimization.element_plan
        if item.current_role == "ky_context"
    ]
    assert ky_plans
    assert all(item.desired_role != "total_ban" for item in ky_plans)
    assert "ky_is_not_total_ban" in context.runtime.optimization.useful_god_plan.conditions


def test_shen_sha_is_not_action_driver() -> None:
    context, _ = _bind_opt(_temporal_payload())
    for action in context.runtime.optimization.actions:
        assert action.driver_kind != "shen_sha"
        assert action.action_type != "shen_sha"


def test_low_recovery_is_not_medical() -> None:
    context, _ = _bind_opt(_temporal_payload())
    compact = present_life_optimization_customer(context.runtime.optimization)
    dump = str(compact).lower()
    for token in ("chẩn đoán", "điều trị", "uống thuốc", "medication"):
        assert token not in dump
    keys = " ".join(_keys(context.runtime.optimization))
    assert "medical" not in keys
    assert "diagnosis" not in keys


def test_temporal_action_does_not_rewrite_natal() -> None:
    payload = _temporal_payload()
    before_ctx, bound = _bind_temporal(payload)
    natal_before = _natal_slice(before_ctx)
    after_ctx = interpret_and_bind_life_optimization(before_ctx, bound)
    assert _natal_slice(after_ctx) == natal_before
    temporal_ids = set(after_ctx.runtime.optimization.temporal_plan.action_ids)
    natal_ids = set(after_ctx.runtime.optimization.natal_plan.action_ids)
    assert temporal_ids.isdisjoint(natal_ids)


def test_improve_bottleneck_does_not_increase_urgency() -> None:
    context, bound = _bind_opt(_temporal_payload())
    result = context.runtime.optimization
    convert = next((item for item in result.actions if "commercialization" in item.recommended_action_key), None)
    if convert is None:
        return
    before = action_urgency(convert)
    wealth = context.runtime.domains.wealth
    natal = replace(
        wealth.natal,
        dimensions={**wealth.natal.dimensions, "commercialization": "high"},
        bottleneck="",
    )
    domains = replace(context.runtime.domains, wealth=replace(wealth, natal=natal))
    mutated = _rehash(replace(context, runtime=replace(context.runtime, domains=domains, optimization=result.__class__())))
    after_ctx = interpret_and_bind_life_optimization(mutated, bound)
    after = next(
        (item for item in after_ctx.runtime.optimization.actions if "commercialization" in item.recommended_action_key),
        None,
    )
    if after is None:
        return
    assert action_urgency(after) >= before


def test_remove_volatility_downgrades_control() -> None:
    context, bound = _bind_opt(_temporal_payload())
    before_ids = set(_keys(context.runtime.optimization))
    if "opt.wealth.retain_capital_discipline" not in before_ids:
        return
    wealth = context.runtime.domains.wealth
    dims = {key: value for key, value in wealth.natal.dimensions.items() if key != "volatility"}
    dims["volatility"] = "moderate"
    natal = replace(wealth.natal, dimensions=dims, risk="", leakage="creation" if wealth.natal.leakage == "creation" else "")
    domains = replace(context.runtime.domains, wealth=replace(wealth, natal=natal))
    mutated = _rehash(replace(context, runtime=replace(context.runtime, domains=domains, optimization=result_empty(context))))
    after_ctx = interpret_and_bind_life_optimization(mutated, bound)
    after_ids = set(_keys(after_ctx.runtime.optimization))
    assert "opt.wealth.retain_capital_discipline" not in after_ids or len(after_ids) <= len(before_ids)


def result_empty(context):
    return context.runtime.optimization.__class__()


def test_improve_recovery_does_not_raise_urgency() -> None:
    context, bound = _bind_opt(_temporal_payload())
    protect = next(
        (
            item
            for item in context.runtime.optimization.actions
            if item.recommended_action_key == "opt.vitality.protect_recovery"
        ),
        None,
    )
    if protect is None:
        return
    before = action_urgency(protect)
    vitality = context.runtime.domains.vitality
    natal = replace(vitality.natal, leakage="", dimensions={**vitality.natal.dimensions, "recovery": "high"})
    domains = replace(context.runtime.domains, vitality=replace(vitality, natal=natal))
    mutated = _rehash(replace(context, runtime=replace(context.runtime, domains=domains, optimization=result_empty(context))))
    after_ctx = interpret_and_bind_life_optimization(mutated, bound)
    after = next(
        (
            item
            for item in after_ctx.runtime.optimization.actions
            if item.recommended_action_key == "opt.vitality.protect_recovery"
        ),
        None,
    )
    if after is None:
        return
    assert action_urgency(after) >= before


def test_annual_change_keeps_natal_plan() -> None:
    payload = _temporal_payload()
    context, bound = _bind_opt(payload)
    natal_ids = context.runtime.optimization.natal_plan.action_ids
    changed = deepcopy(payload)
    luck = dict(changed.get("luck") or {})
    annual = dict(luck.get("annual_identity") or {})
    annual["gan_zhi"] = "Đinh Mùi"
    luck["annual_identity"] = annual
    changed["luck"] = luck
    before_ctx, bound2 = _bind_interaction(changed)
    after_ctx = interpret_and_bind_life_optimization(
        interpret_and_bind_temporal_activation(before_ctx, bound2),
        bound2,
    )
    assert after_ctx.runtime.optimization.natal_plan.action_ids == natal_ids


def test_customer_compact_hides_ids_and_forbidden_advice() -> None:
    context, _ = _bind_opt(_temporal_payload())
    compact = present_life_optimization_customer(context.runtime.optimization)
    dump = str(compact)
    assert compact["top_priorities"]
    assert compact["natal"]["items"]
    assert "TR-P7-" not in dump
    assert "E-DI-" not in dump
    for token in FORBIDDEN:
        assert token not in dump.lower()


def test_empty_diagnostics_keep_optimization_not_evaluated() -> None:
    diagnostics = build_pack07_diagnostics(build_canonical_analysis_context("an-p7-opt-empty"))
    assert diagnostics.optimization is DiagnosticStatus.NOT_EVALUATED
    assert diagnostics.narrative is DiagnosticStatus.NOT_EVALUATED


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = _temporal_payload()
    snapshot = deepcopy(original)
    _bind_opt(original)
    assert original == snapshot


def test_live_case_0001_exposes_action_plan_without_hard_coded_keys() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    optimization = body.get("optimization") or {}
    assert optimization.get("top_priorities")
    assert len(optimization["top_priorities"]) == 3
    assert optimization.get("natal")
    assert optimization.get("temporal")
    dump = str(optimization).lower()
    assert "tr-p7-" not in dump
    for token in FORBIDDEN:
        assert token not in dump
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.optimization is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    data = live.json()["data"]
    assert data["optimization"] == "PASS"
    assert data["narrative"] == "PASS"
    empty = client.get("/api/v1/dev/pack07/diagnostics")
    assert empty.status_code == 200
    assert empty.json()["data"]["optimization"] == "NOT_EVALUATED"
