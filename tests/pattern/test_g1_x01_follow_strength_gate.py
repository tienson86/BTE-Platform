"""G1-X01 follow-pattern Strength gate and cross-engine semantic contract."""

from __future__ import annotations

import json

from applications.api.services.orchestrator import OrchestratorService
from engines.pattern_engine.calculators.follow_pattern import FollowPatternCalculator
from engines.pattern_engine.context import PatternContext
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.follow_tokens import (
    canonicalize_follow_token,
    follow_display_label,
    follow_token_eligible,
)


_WEAK_FOLLOW_FAMILIES: tuple[tuple[str, str, list[str]], ...] = (
    ("tong_tai", "Chính Tài", ["Chính Tài"] * 6 + ["Tỷ Kiên"]),
    ("tong_quan", "Chính Quan", ["Chính Quan"] * 6 + ["Tỷ Kiên"]),
    ("tong_sat", "Thất Sát", ["Thất Sát"] * 6 + ["Tỷ Kiên"]),
    ("tong_nhi", "Thực Thần", ["Thực Thần"] * 6 + ["Tỷ Kiên"]),
)

_REGRESSION_CASES: tuple[tuple[str, dict[str, object]], ...] = (
    ("son", {"year": 1987, "month": 1, "day": 21, "hour": 4, "minute": 30, "gender": "male"}),
    ("huynh", {"year": 1966, "month": 9, "day": 24, "hour": 4, "minute": 15, "gender": "male"}),
    ("dung", {"year": 1982, "month": 5, "day": 22, "hour": 9, "minute": 30, "gender": "female"}),
    ("hung", {"year": 1981, "month": 8, "day": 29, "hour": 4, "minute": 30, "gender": "male"}),
    ("tuyen", {"year": 1984, "month": 7, "day": 13, "hour": 21, "minute": 1, "gender": "female"}),
)

_EXTREME_WEAK_MARKERS = ("cực nhược", "cuc nhuoc", "nhật chủ cực nhược")
_EXTREME_STRONG_MARKERS = ("cực vượng", "cuc vuong", "nhật chủ cực vượng")


def _wealth_context(strength_level: str, gods: list[str] | None = None) -> PatternContext:
    items = gods if gods is not None else ["Chính Tài"] * 6 + ["Tỷ Kiên"]
    return PatternContext(
        day_master="Giáp",
        strength_level=strength_level,
        ten_gods={"list": list(items)},
        ten_gods_list=list(items),
        month_branch_ten_god="Chính Tài",
    )


def _customer_facing_blob(payload: dict) -> str:
    return json.dumps(
        {
            "pattern": payload.get("pattern") or {},
            "useful_god": {
                "winning_rule_id": (payload.get("useful_god") or {}).get("winning_rule_id"),
                "useful_display": (payload.get("useful_god") or {}).get("useful_display"),
                "reasoning": (payload.get("useful_god") or {}).get("reasoning"),
            },
            "interpretation": payload.get("interpretation") or {},
            "report": payload.get("report") or {},
            "narrative": payload.get("narrative") or {},
            "narrative_result": payload.get("narrative_result") or {},
        },
        ensure_ascii=False,
    ).lower()


def test_canonical_token_and_display_are_separate() -> None:
    assert canonicalize_follow_token("Tòng Tài") == "tong_tai"
    assert canonicalize_follow_token("tong_tai") == "tong_tai"
    assert follow_display_label("tong_tai") == "Tòng Tài"
    assert follow_token_eligible("tong_tai", "strong") is False
    assert follow_token_eligible("tong_tai", "balanced") is False
    assert follow_token_eligible("tong_tai", "weak") is True
    assert follow_token_eligible("tong_vuong", "strong") is True
    assert follow_token_eligible("tong_vuong", "weak") is False
    assert follow_token_eligible("tong_vuong", "balanced") is False


def test_strong_with_tai_does_not_become_tong_tai() -> None:
    ctx = _wealth_context("strong")
    assert FollowPatternCalculator().detect(ctx) is None
    result = PatternEngine().calculate(ctx)
    assert result.pattern != "tong_tai"
    assert result.winning_rule_id != "fol_ttai_01"
    assert result.follow_type is None


def test_balanced_with_tai_does_not_become_tong_tai() -> None:
    ctx = _wealth_context("balanced")
    assert FollowPatternCalculator().detect(ctx) is None
    result = PatternEngine().calculate(ctx)
    assert result.pattern != "tong_tai"
    assert result.winning_rule_id != "fol_ttai_01"


def test_weak_with_tai_present_is_not_automatic_tong() -> None:
    ctx = _wealth_context(
        "weak",
        gods=["Chính Tài", "Tỷ Kiên", "Chính Ấn", "Thiên Ấn", "Kiếp Tài"],
    )
    assert FollowPatternCalculator().detect(ctx) is None
    result = PatternEngine().calculate(ctx)
    assert result.pattern != "tong_tai"


def test_weak_with_wealth_dominance_may_become_tong_tai() -> None:
    ctx = _wealth_context("weak")
    assert FollowPatternCalculator().detect(ctx) == "tong_tai"
    result = PatternEngine().calculate(ctx)
    assert result.pattern == "tong_tai"
    assert result.follow_type == "tong_tai"
    assert result.winning_rule_id == "fol_ttai_01"
    assert result.cach_cuc == "Tòng Tài"


def test_other_weak_follow_families_require_weak_strength() -> None:
    detector = FollowPatternCalculator()
    for token, month_god, gods in _WEAK_FOLLOW_FAMILIES:
        weak = PatternContext(
            day_master="Giáp",
            strength_level="weak",
            ten_gods={"list": list(gods)},
            ten_gods_list=list(gods),
            month_branch_ten_god=month_god,
        )
        strong = PatternContext(
            day_master="Giáp",
            strength_level="strong",
            ten_gods={"list": list(gods)},
            ten_gods_list=list(gods),
            month_branch_ten_god=month_god,
        )
        assert detector.detect(weak) == token
        assert detector.detect(strong) is None
        assert PatternEngine().calculate(strong).pattern != token


def test_tong_vuong_not_blocked_by_weak_follow_gate_when_strong() -> None:
    peers = ["Tỷ Kiên"] * 8 + ["Chính Ấn"] * 2
    strong = PatternContext(
        day_master="Giáp",
        strength_level="strong",
        ten_gods={"list": list(peers)},
        ten_gods_list=list(peers),
        month_branch_ten_god="Tỷ Kiên",
    )
    weak = PatternContext(
        day_master="Giáp",
        strength_level="weak",
        ten_gods={"list": list(peers)},
        ten_gods_list=list(peers),
        month_branch_ten_god="Tỷ Kiên",
    )
    detector = FollowPatternCalculator()
    assert detector.detect(strong) == "tong_vuong"
    assert detector.detect(weak) is None
    assert PatternEngine().calculate(strong).pattern == "tong_vuong"
    assert PatternEngine().calculate(weak).pattern != "tong_vuong"


def test_follow_token_publishes_only_when_follow_rule_wins() -> None:
    payload = OrchestratorService().analyze(
        year=1982, month=5, day=22, hour=9, minute=30, gender="female"
    )
    assert payload["strength"]["strength_level"] == "weak"
    assert payload["pattern"]["pattern"] != "tong_tai"
    assert payload["useful_god"]["winning_rule_id"] != "spc_001"


def test_tuyen_strong_rejects_tong_tai() -> None:
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    strength = payload["strength"]
    pattern = payload["pattern"]
    useful = payload["useful_god"]
    assert abs(float(strength["strength_score"]) - 0.66) < 0.005
    assert strength["strength_level"] == "strong"
    assert pattern["pattern"] != "tong_tai"
    assert pattern["winning_rule_id"] != "fol_ttai_01"
    assert "tòng tài" not in str(pattern.get("cach_cuc") or "").lower()
    blob = _customer_facing_blob(payload)
    for marker in _EXTREME_WEAK_MARKERS:
        assert marker not in blob
    assert useful["winning_rule_id"] != "spc_001"


def test_regression_strength_pattern_semantic_contract() -> None:
    for name, kwargs in _REGRESSION_CASES:
        payload = OrchestratorService().analyze(**kwargs)
        level = str(payload["strength"]["strength_level"])
        blob = _customer_facing_blob(payload)
        if payload["pattern"]["pattern"] != "tong_tai":
            assert payload["useful_god"]["winning_rule_id"] != "spc_001"
        if payload["pattern"]["pattern"] != "tong_quan":
            assert payload["useful_god"]["winning_rule_id"] != "spc_002"
        if payload["pattern"]["pattern"] != "tong_sat":
            assert payload["useful_god"]["winning_rule_id"] != "spc_003"
        if level == "strong":
            for marker in _EXTREME_WEAK_MARKERS:
                assert marker not in blob, f"{name} strong claimed {marker}"
            assert payload["pattern"]["pattern"] not in {
                "tong_tai",
                "tong_quan",
                "tong_sat",
                "tong_nhi",
                "tong_an",
            }
        if level == "weak":
            for marker in _EXTREME_STRONG_MARKERS:
                assert marker not in blob, f"{name} weak claimed {marker}"
            assert payload["pattern"]["pattern"] != "tong_vuong"


def test_tuyen_strength_unchanged_and_follow_type_absent() -> None:
    payload = OrchestratorService().analyze(
        year=1984, month=7, day=13, hour=21, minute=1, gender="female"
    )
    assert payload["strength"]["raw_total"] == 16
    assert "follow_type" not in payload["pattern"] or not payload["pattern"].get(
        "follow_type"
    )
