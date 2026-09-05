"""P7-IMP-04 Ten Gods natal interpretation vertical slice."""

from __future__ import annotations

from copy import deepcopy

from engines.detailed_interpretation_engine.builders import (
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.diagnostics import build_pack07_diagnostics, diagnostics_from_payload
from engines.detailed_interpretation_engine.enums import (
    DiagnosticStatus,
    EvaluationStatus,
    TenGodEffectiveStrength,
    TenGodPresenceState,
    TenGodRootState,
)
from engines.detailed_interpretation_engine.ten_gods.constants import CANONICAL_TEN_GOD_IDS, GOD_ID_TO_LABEL
from engines.detailed_interpretation_engine.ten_gods.engine import interpret_and_bind_ten_gods, interpret_ten_gods
from engines.detailed_interpretation_engine.ten_gods.facts import extract_ten_god_facts
from engines.ten_gods_engine.runtime.case_0001 import run_case_0001
from applications.api.services.ten_gods_truth import shape_ten_gods_payload


FORBIDDEN_EXPRESSION_TOKENS = (
    "authority_high",
    "lam_quan",
    "rich",
    "giau",
    "loss",
    "mat_tien",
    "bad",
    "hung",
    "occult",
    "huyen_hoc",
    "hurting_officer_attacks_officer",
    "peer_robs_wealth",
    "owl_robs_food",
)


def _item(god_id: str, **fields: object) -> dict[str, object]:
    return {
        "pillar": "year",
        "stem": "Giáp",
        "ten_god": GOD_ID_TO_LABEL[god_id],
        "god_id": god_id,
        "element": "Mộc",
        **fields,
    }


def _payload(*, visible: list | None = None, hidden: list | None = None, **extra: object) -> dict[str, object]:
    return {
        "analysis_id": "an-p7-tg-001",
        "pattern": {"cach_cuc": extra.pop("pattern", "Chính Ấn"), "pattern": extra.get("pattern_id", "")},
        "score": {"grade": "B"},
        "strength": {"strength_level": extra.pop("strength_level", "balanced")},
        "useful_god": extra.pop("useful_god", {"useful_display": "Thủy"}),
        "ten_gods": {
            "source": "engines.ten_gods_engine",
            "visible": visible or [],
            "hidden": hidden or [],
        },
        **extra,
    }


def _by_id(collection, god_id: str):
    return next(item for item in collection.items if item.ten_god_id == god_id)


def test_all_ten_gods_are_represented() -> None:
    collection = interpret_ten_gods(_payload(), analysis_id="an-p7-tg-001")
    assert tuple(item.ten_god_id for item in collection.items) == CANONICAL_TEN_GOD_IDS
    assert all(item.presence_state is TenGodPresenceState.ABSENT for item in collection.items)


def test_absent_hidden_only_visible_rootless_and_rooted() -> None:
    payload = _payload(
        visible=[
            _item("zheng_guan", pillar="month"),
            _item("shi_shen", pillar="year"),
        ],
        hidden=[
            {
                "pillar": "month",
                "branch": "Thìn",
                "hidden_stem": "Ất",
                "position_name": "primary",
                "hidden_position": 1,
                "ten_god": "Chính Quan",
                "god_id": "zheng_guan",
                "element": "Mộc",
            },
            {
                "pillar": "hour",
                "branch": "Hợi",
                "hidden_stem": "Nhâm",
                "position_name": "tertiary",
                "hidden_position": 3,
                "ten_god": "Kiếp Tài",
                "god_id": "jie_cai",
                "element": "Thủy",
            },
        ],
    )
    collection = interpret_ten_gods(payload, analysis_id="an-p7-tg-001")
    assert _by_id(collection, "bi_jian").presence_state is TenGodPresenceState.ABSENT
    hidden_only = _by_id(collection, "jie_cai")
    assert hidden_only.presence_state is TenGodPresenceState.HIDDEN_ONLY
    rootless = _by_id(collection, "shi_shen")
    assert rootless.presence_state is TenGodPresenceState.VISIBLE
    assert rootless.root_state is TenGodRootState.NO_ROOT
    rooted = _by_id(collection, "zheng_guan")
    assert rooted.presence_state in {
        TenGodPresenceState.VISIBLE_AND_ROOTED,
        TenGodPresenceState.CONCENTRATED,
        TenGodPresenceState.REPEATED,
    }
    assert rooted.root_state in {TenGodRootState.STRONG_ROOT, TenGodRootState.MULTIPLE_ROOTS}


def test_weak_and_strong_effective_strength() -> None:
    payload = _payload(
        visible=[_item("pian_cai", pillar="year")],
        hidden=[
            {
                "pillar": "month",
                "branch": "Tỵ",
                "hidden_stem": "Bính",
                "position_name": "primary",
                "hidden_position": 1,
                "ten_god": "Thiên Tài",
                "god_id": "pian_cai",
                "element": "Hỏa",
            },
            {
                "pillar": "hour",
                "hidden_stem": "Đinh",
                "position_name": "secondary",
                "hidden_position": 2,
                "ten_god": "Thiên Tài",
                "god_id": "pian_cai",
                "element": "Hỏa",
            },
        ],
        strength_level="weak",
    )
    payload["ten_gods"]["visible"].append(_item("zheng_yin", pillar="hour"))
    collection = interpret_ten_gods(payload, analysis_id="an-p7-tg-001")
    wealth = _by_id(collection, "pian_cai")
    assert wealth.effective_strength in {
        TenGodEffectiveStrength.MODERATE,
        TenGodEffectiveStrength.STRONG,
        TenGodEffectiveStrength.VERY_STRONG,
    }
    seal = _by_id(collection, "zheng_yin")
    assert seal.effective_strength in {
        TenGodEffectiveStrength.WEAK,
        TenGodEffectiveStrength.VERY_WEAK,
        TenGodEffectiveStrength.MODERATE,
    }


def test_unresolved_when_upstream_facts_missing() -> None:
    collection = interpret_ten_gods({"analysis_id": "an-p7-tg-miss"}, analysis_id="an-p7-tg-miss")
    assert collection.state is EvaluationStatus.UNRESOLVED
    assert all(item.presence_state is TenGodPresenceState.UNRESOLVED for item in collection.items)


def test_negative_presence_is_not_dictionary_outcome() -> None:
    payload = _payload(
        visible=[
            _item("zheng_guan", pillar="year"),
            _item("pian_cai", pillar="month"),
            _item("jie_cai", pillar="hour"),
            _item("qi_sha", pillar="year", stem="Bính"),
            _item("pian_yin", pillar="month", stem="Ất"),
            _item("shang_guan", pillar="hour", stem="Đinh"),
        ]
    )
    collection = interpret_ten_gods(payload, analysis_id="an-p7-tg-001")
    joined = " ".join(
        " ".join(item.positive_expressions + item.risk_expressions + item.damage_ids + item.rescue_ids)
        for item in collection.items
    )
    for token in FORBIDDEN_EXPRESSION_TOKENS:
        assert token not in joined
    officer = _by_id(collection, "zheng_guan")
    assert officer.presence_state is not TenGodPresenceState.ABSENT
    assert "authority_high" not in officer.positive_expressions
    assert _by_id(collection, "jie_cai").damage_ids == ()
    assert _by_id(collection, "shang_guan").damage_ids == ()
    assert _by_id(collection, "qi_sha").structural_usability.value != "damaging"


def test_mc01_boundary_does_not_elect_or_mutate_structure() -> None:
    original = _payload(visible=[_item("zheng_guan", pillar="month")])
    snapshot = deepcopy(original)
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(original),
        original,
    )
    assert original == snapshot
    natal = context.runtime.interpretation.ten_gods.natal
    officer = _by_id(natal, "zheng_guan")
    assert officer.damage_ids == ()
    assert officer.rescue_ids == ()
    assert context.runtime.mc01.mingju_result_id == ""
    assert context.interpretation.grade_ref == "B"
    assert "pattern" not in context.runtime.interpretation.ten_gods.finding_ids


def test_useful_god_is_consumed_not_calculated() -> None:
    payload = _payload(
        visible=[_item("zheng_yin", pillar="year")],
        useful_god={"useful_ten_god": "Chính Ấn", "useful_element": "Thổ"},
    )
    collection = interpret_ten_gods(payload, analysis_id="an-p7-tg-001")
    seal = _by_id(collection, "zheng_yin")
    assert seal.useful_god_context.value in {"useful", "favorable", "neutral"}
    wealth = _by_id(collection, "pian_cai")
    assert wealth.useful_god_context.value != "useful"


def test_case_0001_uses_upstream_identity_facts() -> None:
    shaped = shape_ten_gods_payload(run_case_0001())
    payload = _payload()
    payload["ten_gods"] = shaped
    payload["analysis_id"] = "CASE-0001"
    facts = extract_ten_god_facts(payload)
    collection = interpret_ten_gods(payload, analysis_id="CASE-0001")
    assert collection.state is EvaluationStatus.PARTIALLY_RESOLVED
    present_ids = {
        item.ten_god_id
        for item in collection.items
        if item.presence_state is not TenGodPresenceState.ABSENT
    }
    fact_ids = {god_id for god_id, items in facts.occurrences.items() if items}
    assert present_ids == fact_ids
    assert "thien_quan" not in present_ids
    assert any(item.ten_god_id == "qi_sha" for item in collection.items)


def test_runtime_binding_and_diagnostics_partial() -> None:
    payload = _payload(visible=[_item("zheng_guan", pillar="month")])
    context = interpret_and_bind_ten_gods(
        build_canonical_analysis_context_from_payload(payload),
        payload,
    )
    natal = context.runtime.interpretation.ten_gods.natal
    assert natal.analysis_id == "an-p7-tg-001"
    assert len(natal.items) == 10
    diagnostics = build_pack07_diagnostics(context)
    assert diagnostics.ten_gods is DiagnosticStatus.PARTIAL
    assert diagnostics.shen_sha is DiagnosticStatus.NOT_IMPLEMENTED
    empty = build_pack07_diagnostics(build_canonical_analysis_context_from_payload({"analysis_id": "dev-empty"}))
    assert empty.ten_gods is DiagnosticStatus.NOT_IMPLEMENTED


def test_no_thien_quan_alias_identity() -> None:
    payload = _payload(
        visible=[{"pillar": "year", "ten_god": "Thiên Quan", "god_id": "thien_quan"}]
    )
    collection = interpret_ten_gods(payload, analysis_id="an-p7-tg-001")
    ids = [item.ten_god_id for item in collection.items]
    assert "thien_quan" not in ids
    assert _by_id(collection, "qi_sha").presence_state is not TenGodPresenceState.ABSENT


def test_analyze_payload_diagnostics_from_shaped_facts() -> None:
    payload = _payload(visible=[_item("shi_shen", pillar="hour")])
    diagnostics = diagnostics_from_payload(payload)
    assert diagnostics.ten_gods is DiagnosticStatus.PARTIAL
    assert diagnostics.contracts is DiagnosticStatus.PASS
    assert diagnostics.runtime_contract is DiagnosticStatus.PASS
