"""PAT-R1F: LEVEL-1 special Pattern must not enter spc_* Overall competition."""

from __future__ import annotations

from engines.bazi_engine.engine import BaziChart, HIDDEN, Pillar
from engines.bazi_engine.ten_god import ten_god_name
from engines.pattern_engine.engine import PatternEngine
from engines.pattern_engine.override_eligibility import classify_pattern_override
from engines.pattern_engine.utils.context_builder import build_pattern_context
from engines.useful_god_engine.engine import UsefulGodEngine
from engines.useful_god_engine.utils.context_builder import build_useful_god_context


def _dung_chart() -> BaziChart:
    year = Pillar(stem="Ất", branch="Sửu")
    month = Pillar(stem="Ất", branch="Dậu")
    day = Pillar(stem="Canh", branch="Thân")
    hour = Pillar(stem="Canh", branch="Thìn")
    pillars = [year, month, day, hour]
    hidden = [stem for pillar in pillars for stem in HIDDEN[pillar.branch]]
    dm = day.stem
    ten_gods = [
        "Nhật Chủ" if pillar is day else ten_god_name(dm, pillar.stem) for pillar in pillars
    ]
    return BaziChart(*pillars, gender="male", hidden_stems=hidden, ten_gods=ten_gods)


def test_level_1_special_is_detected_not_override_eligible() -> None:
    result = classify_pattern_override("gia_sac", None)
    assert result.qualification_level == 1
    assert result.ug_override_eligible is False
    assert result.detected_special_pattern == "gia_sac"


def test_published_follow_remains_override_eligible() -> None:
    result = classify_pattern_override("tong_tai", "tong_tai")
    assert result.qualification_level == 2
    assert result.ug_override_eligible is True
    assert result.follow_pattern == "tong_tai"


def test_dung_gia_sac_detected_but_spc_004_not_in_overall() -> None:
    chart = _dung_chart()
    context = build_pattern_context(chart)
    context.strength_level = "strong"
    context.strength_score = 1.0
    pattern = PatternEngine().calculate(context)
    assert pattern.pattern == "gia_sac"
    assert pattern.ug_override_eligible is False
    assert pattern.qualification_level == 1
    assert "Giá Sắc" in (pattern.cach_cuc or "")
    assert "nhận diện" in (pattern.cach_cuc or "")

    useful = UsefulGodEngine().calculate(build_useful_god_context(context, pattern))
    overall_ids = [
        str(item.get("rule_id") or "") for item in useful.overall_candidate_list
    ]
    assert "spc_004" not in overall_ids
    assert useful.winning_rule_id != "spc_004"
    assert "spc_004" not in list(useful.matched_rules or [])
    assert useful.winning_rule_group == "strength"
