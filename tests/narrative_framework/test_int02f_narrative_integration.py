"""INT-02F Narrative Integration tests. No engine execution."""

from __future__ import annotations

from pathlib import Path

from engines.narrative_framework.contracts import INSUFFICIENT_COPY
from engines.narrative_framework.integration import (
    INTEGRATED_BLOCKS,
    compose_integrated_narrative,
)
from engines.narrative_framework.luck import compose_luck_narrative
from engines.narrative_framework.pattern import compose_pattern_narrative
from engines.narrative_framework.strength import compose_strength_narrative
from engines.narrative_framework.useful_god import compose_useful_god_narrative

INTEGRATION_DIR = (
    Path(__file__).resolve().parents[2] / "engines" / "narrative_framework" / "integration"
)

SAMPLE_STRENGTH = {
    "strength_level": "strong",
    "strength_score": 0.87,
    "season_score": 0.4,
    "root_score": 0.3,
    "support_score": 0.2,
    "control_score": 0.1,
    "drain_score": 0.05,
    "confidence": 0.8,
    "reasoning": "Đắc lệnh tháng và thông căn nên lực Nhật chủ vững",
    "evidence_compact": "Đắc lệnh +4 · Thông căn +3",
}

SAMPLE_USEFUL_GOD = {
    "useful_god": "Hỏa",
    "useful_display": "Hỏa · Đinh · Chính Quan",
    "useful_ten_god": "Chính Quan",
    "favorable_display": "Thổ · Mậu · Thiên Ấn",
    "unfavorable_display": "Tỷ Kiên · Kiếp Tài",
    "reasoning": "Thân nhược nên lấy Hỏa Chính Quan làm Dụng thần",
    "recommendations": ["Ưu tiên hướng Hỏa đã công bố"],
    "climate_preference_label": "Cần ôn",
}

SAMPLE_TEMPERATURE = {
    "climate_state_label": "Hàn",
    "balancing_need_label": "Cần ôn",
    "recommendations": ["Ưu tiên môi trường ấm đã công bố"],
}

SAMPLE_PATTERN = {
    "pattern": "chinh_quan",
    "cach_cuc": "Chính Quan",
    "dieu_hau": "Cần ôn",
    "reason": "Tháng lệnh Chính Quan nên lập cách Chính Quan",
    "dung_than": "Hỏa",
    "hy_than": "Thổ",
    "recommendations": ["Giữ trục Chính Quan đã công bố"],
}

SAMPLE_LUCK = {
    "current_dayun": {"index": 3, "start_age": 32, "ganzhi": "Giáp Thìn"},
    "current_liunian": {"year": 2026, "ganzhi": "Bính Ngọ"},
    "timeline": "Đại Vận Giáp Thìn · Lưu Niên Bính Ngọ",
    "luck_stage": "vượng",
    "luck_summary": "Đại Vận Giáp Thìn đang chạy, Lưu Niên Bính Ngọ tiếp nhịp",
    "recommendations": ["Giữ nhịp Đại Vận đã công bố"],
}


def _units():
    strength = compose_strength_narrative(
        SAMPLE_STRENGTH,
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    useful = compose_useful_god_narrative(SAMPLE_USEFUL_GOD)
    pattern = compose_pattern_narrative(
        SAMPLE_PATTERN,
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    luck = compose_luck_narrative(SAMPLE_LUCK)
    return strength, useful, pattern, luck


def _topic_sentences(units) -> list[str]:
    texts: list[str] = []
    for unit in units:
        for slot in ("observation", "reasoning", "impact", "recommendation"):
            texts.extend(getattr(unit, slot).sentences)
    return texts


def test_merge_includes_four_topics_in_order() -> None:
    """Integrated unit consumes Strength, Useful God, Pattern, then Luck."""
    unit = compose_integrated_narrative(*_units())
    assert unit.topics == ("strength", "useful_god", "pattern", "luck")
    assert unit.to_dict()["block_order"] == list(INTEGRATED_BLOCKS)
    assert unit.status == "complete"


def test_executive_summary_uses_published_topic_leads_only() -> None:
    """Executive summary is the first observation of each topic. No new facts."""
    strength, useful, pattern, luck = _units()
    unit = compose_integrated_narrative(strength, useful, pattern, luck)
    exec_text = " ".join(unit.executive_summary.sentences)
    assert unit.executive_summary.available is True
    assert strength.observation.sentences[0] in unit.executive_summary.sentences
    assert useful.observation.sentences[0] in unit.executive_summary.sentences
    assert pattern.observation.sentences[0] in unit.executive_summary.sentences
    assert luck.observation.sentences[0] in unit.executive_summary.sentences
    assert exec_text.count("Thân vượng") == 1
    assert "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan" in exec_text


def test_deduplicate_does_not_repeat_strength_or_useful_god_naming() -> None:
    """Lead facts are not restated after the executive summary."""
    unit = compose_integrated_narrative(*_units())
    body = " ".join(
        unit.observation.sentences + unit.reasoning.sentences + unit.impact.sentences
    )
    assert "Nhật chủ được đọc là Thân vượng." not in unit.observation.sentences
    assert body.count("Nhật chủ được đọc là Thân vượng") == 0
    assert "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan." not in unit.observation.sentences
    assert "Phân loại lực đã công bố vẫn là Thân vượng." not in unit.reasoning.sentences


def test_recommendation_merge_keeps_unique_published_advice() -> None:
    """Duplicate Dụng thần advice collapses; distinct topic recs remain."""
    strength, useful, pattern, luck = _units()
    unit = compose_integrated_narrative(strength, useful, pattern, luck)
    recs = unit.recommendation.sentences
    joined = " ".join(recs)
    assert recs.count("Ưu tiên hướng Dụng thần đã công bố: Hỏa · Đinh · Chính Quan.") == 1
    assert joined.count("Ưu tiên hướng Dụng thần đã công bố") == 1
    assert "Giữ trục Chính Quan đã công bố" in joined
    assert "Giữ nhịp Đại Vận đã công bố" in joined
    assert "useful_god" in unit.recommendation.topic_ids or "strength" in unit.recommendation.topic_ids


def test_integrated_sentences_introduce_no_new_facts() -> None:
    """Every integrated speech sentence already exists on a topic unit."""
    units = _units()
    integrated = compose_integrated_narrative(*units)
    published = _topic_sentences(units)
    for slot in ("executive_summary", "observation", "reasoning", "impact", "recommendation"):
        for sentence in getattr(integrated, slot).sentences:
            assert sentence in published


def test_empty_topics_are_insufficient() -> None:
    """No topic units yield an honest empty integrated narrative."""
    unit = compose_integrated_narrative()
    assert unit.status == "insufficient"
    assert unit.executive_summary.insufficient is True
    assert unit.observation.insufficient is True
    assert unit.recommendation.to_dict()["empty_copy"] == INSUFFICIENT_COPY


def test_summary_synthesizes_merged_blocks_only() -> None:
    """Summary joins first sentences of the merged speech blocks."""
    unit = compose_integrated_narrative(*_units())
    assert unit.summary.available is True
    prior = " ".join(
        unit.observation.sentences
        + unit.reasoning.sentences
        + unit.impact.sentences
        + unit.recommendation.sentences
    )
    for fragment in unit.summary.sentences[0].rstrip(".").split(". "):
        assert fragment.strip() in prior


def test_integration_does_not_recalculate_or_touch_delivery() -> None:
    """INT-02F must not import engines, Workspace, or Report."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in INTEGRATION_DIR.glob("*.py"))
    assert "LuckEngine" not in joined
    assert "StrengthEngine" not in joined
    assert "UsefulGodEngine" not in joined
    assert "PatternEngine" not in joined
    assert "def calculate(" not in joined
    assert "calculators" not in joined
    assert "customer_portal" not in joined
    assert "report_engine" not in joined
    assert "Workspace" not in joined
    assert "good_score" not in joined
