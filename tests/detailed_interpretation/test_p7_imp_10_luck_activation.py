"""P7-IMP-10 Luck Activation Engine: expression opportunity, not natal rewrite."""

from __future__ import annotations

from copy import deepcopy

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.detailed_interpretation_engine.diagnostics import diagnostics_from_payload
from engines.detailed_interpretation_engine.enums import ActivationState, DiagnosticStatus
from engines.detailed_interpretation_engine.luck_activation.constants import MAIN_ACTIVATION_IDS, STATE_RANK
from engines.detailed_interpretation_engine.luck_activation.engine import (
    interpret_and_bind_luck_activation,
)
from engines.detailed_interpretation_engine.serialization import to_jsonable
from engines.detailed_interpretation_engine.validators import validate_luck_activation_result
from tests.detailed_interpretation.test_p7_imp_09_domains import CASE_0001, _bind, _payload

MAIN = MAIN_ACTIVATION_IDS


def _luck_cycle(
    *,
    stem: str = "Quý",
    branch: str = "Mão",
    gan_zhi: str = "Quý Mão",
    stem_element: str = "Thủy",
    branch_element: str = "Mộc",
    year_start: int = 2021,
    year_end: int = 2030,
    index: int = 3,
) -> dict[str, object]:
    return {
        "index": index,
        "stem": stem,
        "branch": branch,
        "gan_zhi": gan_zhi,
        "stem_element": stem_element,
        "branch_element": branch_element,
        "year_start": year_start,
        "year_end": year_end,
    }


def _luck_payload(
    cycle: dict[str, object] | None = None,
    *,
    attack: tuple[str, ...] = (),
) -> dict[str, object]:
    payload = _payload()
    pattern = dict(payload.get("pattern") or {})
    pattern["day_master"] = "Đinh"
    payload["pattern"] = pattern
    identity = dict(payload.get("identity") or {})
    pillars = dict(identity.get("four_pillars") or {})
    pillars["day"] = {"stem": "Đinh", "branch": "Sửu"}
    identity["four_pillars"] = pillars
    payload["identity"] = identity
    payload["luck"] = {
        "current_cycle": cycle or _luck_cycle(),
        "support_elements": ["Thủy"],
        "attack_elements": list(attack),
    }
    return payload


def _bind_domains(payload: dict[str, object]):
    return _bind(payload)


def _bind_luck(payload: dict[str, object]):
    context, bound = _bind_domains(payload)
    return interpret_and_bind_luck_activation(context, bound), bound


def _natal_slice(context) -> object:
    runtime = context.runtime
    return to_jsonable(
        {
            "mc01": context.interpretation.mc01,
            "domains": runtime.domains,
            "evidence_priority": runtime.interpretation.evidence_priority,
            "ten_gods": runtime.interpretation.ten_gods.natal,
            "combinations": runtime.interpretation.ten_gods.combinations,
            "ecosystem": runtime.interpretation.ten_gods.ecosystem,
            "shen_sha": runtime.interpretation.shen_sha.individual,
            "shen_eco": runtime.interpretation.shen_sha.ecosystem,
        }
    )


def test_six_main_domains_receive_activation() -> None:
    context, _ = _bind_luck(_luck_payload())
    result = context.runtime.temporal.luck_activation
    assert result.time_window == "2021–2030"
    assert result.cycle_id
    for domain_id in MAIN:
        item = result.items[domain_id]
        assert item.domain_id == domain_id
        assert item.activation_state is not None
        assert item.natal_state
        assert item.natal_driver_id
        assert item.activation_driver_id != item.natal_driver_id or item.activation_driver_id in {
            "not_applicable",
            "unresolved",
        }
    issues = validate_luck_activation_result(result, context=context)
    assert not issues.errors


def test_luck_does_not_mutate_natal_slices() -> None:
    payload = _luck_payload()
    before_ctx, bound = _bind_domains(payload)
    before = _natal_slice(before_ctx)
    after_ctx = interpret_and_bind_luck_activation(before_ctx, bound)
    assert _natal_slice(after_ctx) == before
    for domain_id in MAIN:
        natal = getattr(after_ctx.runtime.domains, domain_id).natal
        item = after_ctx.runtime.temporal.luck_activation.items[domain_id]
        assert natal.state.value == item.natal_state
        assert natal.driver_id == item.natal_driver_id
        assert natal.bottleneck == item.natal_bottleneck


def test_luck_cannot_change_pattern_or_grade() -> None:
    payload = _luck_payload()
    before_ctx, bound = _bind_domains(payload)
    pattern = before_ctx.interpretation.pattern_ref
    grade = before_ctx.interpretation.grade_ref
    after_ctx = interpret_and_bind_luck_activation(before_ctx, bound)
    assert after_ctx.interpretation.pattern_ref == pattern
    assert after_ctx.interpretation.grade_ref == grade
    assert "pattern" not in after_ctx.runtime.temporal.luck_activation.items


def test_temporal_ten_god_is_not_natal_ten_god() -> None:
    before_ctx, bound = _bind_domains(_luck_payload())
    before_ids = tuple(item.ten_god_id for item in before_ctx.runtime.interpretation.ten_gods.natal.items)
    context = interpret_and_bind_luck_activation(before_ctx, bound)
    luck = context.runtime.temporal.luck_activation
    after_ids = tuple(item.ten_god_id for item in context.runtime.interpretation.ten_gods.natal.items)
    assert luck.temporal_ten_god
    assert luck.temporal_stem == "Quý"
    assert after_ids == before_ids
    assert luck.temporal_ten_god not in after_ids
    assert all(item.activation_driver_id != "hybrid" for item in luck.items.values())


def test_useful_god_match_is_not_automatic_peak() -> None:
    context, _ = _bind_luck(_luck_payload())
    luck = context.runtime.temporal.luck_activation
    assert any(item.natal_state in {"conditional", "fragmented", "weak"} for item in luck.items.values())
    for item in luck.items.values():
        if item.natal_state in {"conditional", "fragmented", "weak"}:
            assert item.activation_state is not ActivationState.PEAK


def test_clash_is_not_automatic_suppressed() -> None:
    context, _ = _bind_luck(_luck_payload(attack=("Hỏa",)))
    wealth = context.runtime.temporal.luck_activation.items["wealth"]
    assert wealth.activation_state is not ActivationState.SUPPRESSED


def test_strong_activation_is_not_an_event() -> None:
    context, _ = _bind_luck(_luck_payload())
    luck = context.runtime.temporal.luck_activation
    for item in luck.items.values():
        if item.activation_state in {ActivationState.STRONG, ActivationState.PEAK, ActivationState.OVERLOADED}:
            assert "not_an_event_prediction" in item.warnings


def test_changing_luck_cycle_leaves_natal_identical() -> None:
    first, _ = _bind_luck(_luck_payload(_luck_cycle()))
    second, _ = _bind_luck(
        _luck_payload(
            _luck_cycle(
                stem="Giáp",
                branch="Thìn",
                gan_zhi="Giáp Thìn",
                stem_element="Mộc",
                branch_element="Thổ",
                year_start=2031,
                year_end=2040,
                index=4,
            )
        )
    )
    assert _natal_slice(first) == _natal_slice(second)
    assert first.runtime.temporal.luck_activation.cycle_id != second.runtime.temporal.luck_activation.cycle_id


def test_temporal_support_does_not_worsen_unless_overload() -> None:
    dormant, _ = _bind_luck(
        _luck_payload(
            _luck_cycle(
                stem="Tân",
                branch="Dậu",
                gan_zhi="Tân Dậu",
                stem_element="Kim",
                branch_element="Kim",
            )
        )
    )
    supported, _ = _bind_luck(
        _luck_payload(
            _luck_cycle(
                stem="Ất",
                branch="Mão",
                gan_zhi="Ất Mão",
                stem_element="Mộc",
                branch_element="Mộc",
            )
        )
    )
    before = dormant.runtime.temporal.luck_activation.items["vitality"]
    after = supported.runtime.temporal.luck_activation.items["vitality"]
    if after.activation_state is not ActivationState.OVERLOADED:
        assert STATE_RANK[after.activation_state] >= STATE_RANK[before.activation_state]


def test_excess_activation_may_overload_carrying_capacity() -> None:
    context, _ = _bind_luck(_luck_payload())
    authority = context.runtime.temporal.luck_activation.items["authority"]
    assert authority.natal_state in {"conditional", "fragmented", "weak", "moderate", "strong", "very_strong"}
    if authority.natal_state in {"conditional", "fragmented", "weak"}:
        assert authority.activation_state is not ActivationState.PEAK


def test_removing_luck_leaves_natal_identical() -> None:
    payload = _payload()
    before_ctx, bound = _bind_domains(payload)
    before = _natal_slice(before_ctx)
    after_ctx = interpret_and_bind_luck_activation(before_ctx, bound)
    assert _natal_slice(after_ctx) == before
    assert after_ctx.runtime.temporal.luck_activation.status.value == "not_applicable"


def test_activation_graph_is_luck_to_domain_only() -> None:
    context, _ = _bind_luck(_luck_payload())
    graph = context.runtime.temporal.luck_activation.graph
    assert graph.nodes
    for edge in graph.edges:
        assert edge.source not in MAIN
        assert edge.target in set(MAIN) | {
            "creative",
            "academic",
            "leadership",
            "management",
            "learning",
            "personal_growth",
        }


def test_live_case_0001_keeps_natal_and_exposes_activation() -> None:
    client = TestClient(create_app())
    analyzed = client.post("/api/v1/analyze", json=CASE_0001)
    assert analyzed.status_code == 200
    body = analyzed.json()["data"]
    domains = {item["id"]: item for item in (body.get("domains") or {}).get("items") or []}
    assert set(domains) >= set(MAIN)
    luck = body.get("luck") or {}
    activation = luck.get("activation") or {}
    items = {item["id"]: item for item in activation.get("items") or []}
    assert set(items) >= set(MAIN)
    assert "–" in str(activation.get("time_window") or luck.get("current_cycle", {}).get("year_start") or "–")
    assert "TR-P7-" not in str(activation)
    assert "E-DI-" not in str(activation)
    assert body.get("pattern", {}).get("structural_grade") == "B"
    diagnostics = diagnostics_from_payload(body)
    assert diagnostics.domains is DiagnosticStatus.PASS
    assert diagnostics.luck is DiagnosticStatus.PASS
    live = client.post("/api/v1/dev/pack07/diagnostics", json=CASE_0001)
    assert live.status_code == 200
    assert live.json()["data"]["luck"] == "PASS"
    assert live.json()["data"]["domains"] == "PASS"


def test_payload_builders_do_not_mutate_upstream() -> None:
    original = _luck_payload()
    snapshot = deepcopy(original)
    _bind_luck(original)
    assert original == snapshot
