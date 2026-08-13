"""Useful God stem location and Hỷ/Kỵ mapping into RuleContext."""

from __future__ import annotations

from engines.rule_contract.context_builder import RuleContextBuilder
from engines.useful_god_engine.models import UsefulGodResult


def _huynh_bazi() -> dict[str, object]:
    return {
        "day_master": "Bính",
        "month_branch": "Dậu",
        "year_pillar": {"stem": "Bính", "branch": "Ngọ"},
        "month_pillar": {"stem": "Đinh", "branch": "Dậu"},
        "day_pillar": {"stem": "Bính", "branch": "Tuất"},
        "hour_pillar": {"stem": "Canh", "branch": "Dần"},
    }


def test_favorable_gods_survive_rule_context_mapping() -> None:
    """C. UsefulGodResult.favorable_gods survives RuleContext mapping."""
    result = UsefulGodResult(
        useful_god="Đinh",
        favorable_gods=["Đinh", "Bính", "Ất"],
        unfavorable_gods=["Canh", "Tân"],
        confidence=0.85,
        matched_rules=["sea_004"],
    )
    mapped = RuleContextBuilder()._build_useful_god(
        None,
        result,
        {},
        _huynh_bazi(),
        {},
        {},
    )
    assert mapped["favorable_gods"] == ["Đinh", "Bính", "Ất"]
    assert mapped["favorable"] == ["Đinh", "Bính", "Ất"]


def test_unfavorable_gods_survive_rule_context_mapping() -> None:
    """D. UsefulGodResult.unfavorable_gods survives RuleContext mapping."""
    result = UsefulGodResult(
        useful_god="Đinh",
        favorable_gods=["Đinh", "Bính", "Ất"],
        unfavorable_gods=["Canh", "Tân"],
    )
    mapped = RuleContextBuilder()._build_useful_god(
        None,
        result,
        {},
        _huynh_bazi(),
        {},
        {},
    )
    assert mapped["unfavorable_gods"] == ["Canh", "Tân"]
    assert mapped["unfavorable"] == ["Canh", "Tân"]


def test_stem_useful_god_uses_stem_aware_locator() -> None:
    """E. Stem Useful God values are located as stems, including Chinese aliases."""
    builder = RuleContextBuilder()
    bazi = _huynh_bazi()
    dinh = builder._locate_useful_god("Đinh", "stem", bazi, {}, {})
    assert dinh["in_stem"] is True
    han = builder._locate_useful_god("丁", "stem", bazi, {}, {})
    assert han["in_stem"] is True
    canh = builder._locate_useful_god("Canh", "stem", bazi, {}, {})
    assert canh["in_stem"] is True
    giap = builder._locate_useful_god("Giáp", "stem", bazi, {}, {})
    assert giap["in_hidden"] is True
    binh = builder._locate_useful_god("Bính", "stem", bazi, {}, {})
    assert binh["in_stem"] is True


def test_present_stem_does_not_produce_missing_status() -> None:
    """F. A present stem Useful God does not produce 'Không có Dụng thần'."""
    result = UsefulGodResult(
        useful_god="Đinh",
        favorable_gods=["Đinh", "Bính", "Ất"],
        unfavorable_gods=["Canh", "Tân"],
    )
    mapped = RuleContextBuilder()._build_useful_god(
        None,
        result,
        {},
        _huynh_bazi(),
        {},
        {},
    )
    assert mapped["name"] == "Đinh"
    assert mapped["candidate_type"] == "stem"
    assert mapped["in_stem"] is True
    assert mapped["status"] != "Không có Dụng thần"
    assert "Không có Dụng thần" not in str(mapped["status"])


def test_ten_god_candidate_still_uses_ten_god_locator() -> None:
    """Ten-god Useful God names keep role lookup, not stem matching."""
    builder = RuleContextBuilder()
    bazi = _huynh_bazi()
    mapped = builder._build_useful_god(
        None,
        UsefulGodResult(useful_god="Thiên Tài"),
        {},
        bazi,
        {},
        {"unique": ["Thiên Tài"]},
    )
    assert mapped["candidate_type"] == "ten_god"
    assert mapped["in_stem"] is True
    assert mapped["status"] != "Không có Dụng thần"
