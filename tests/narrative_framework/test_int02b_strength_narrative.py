"""INT-02B Strength Narrative tests. No Strength Engine execution."""

from __future__ import annotations

from pathlib import Path

from engines.narrative_framework.strength import (
    STRENGTH_BLOCKS,
    bind_strength_evidence,
    build_impact,
    build_observation,
    build_reasoning,
    build_recommendation,
    compose_strength_narrative,
)
from engines.strength_engine.models import StrengthResult

STRENGTH_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_framework" / "strength"

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
    "metadata": {"trace": {"analysis": {"special_matches": ["STR-SPECIAL-01"]}}},
}

SAMPLE_USEFUL_GOD = {
    "useful_display": "Hỏa · Đinh · Chính Quan",
    "useful_god": "Hỏa",
    "favorable_display": "Thổ",
}

SAMPLE_TEMPERATURE = {
    "climate_state_label": "Hàn",
    "balancing_need_label": "Cần ôn",
    "recommendations": ["Ưu tiên môi trường ấm đã công bố"],
}


def test_evidence_copies_published_strength_fields() -> None:
    """Evidence is a copy of Strength output, not a rescore."""
    evidence = bind_strength_evidence(SAMPLE_STRENGTH, temperature=SAMPLE_TEMPERATURE)
    assert evidence.strength_level == "strong"
    assert evidence.score == 0.87
    assert evidence.season_strength == 0.4
    assert evidence.root_strength == 0.3
    assert evidence.support_strength == 0.2
    assert evidence.control_strength == 0.1
    assert evidence.drain_strength == 0.05
    assert evidence.confidence == 0.8
    assert evidence.special_rules == ("STR-SPECIAL-01",)
    assert evidence.temperature_state == "Hàn"
    assert "strength_level" not in evidence.missing


def test_observation_uses_evidence_only() -> None:
    """Observation names the class and score. It does not advise."""
    evidence = bind_strength_evidence(SAMPLE_STRENGTH)
    block = build_observation(evidence)
    assert block.available is True
    assert block.sentences[0] == "Nhật chủ được đọc là Thân vượng."
    assert "0.87" in block.sentences[1]
    joined = " ".join(block.sentences)
    assert "Ưu tiên" not in joined
    assert "Kết luận" not in joined


def test_reasoning_explains_published_evidence() -> None:
    """Reasoning restates published reasoning and grouped classified evidence."""
    evidence = bind_strength_evidence(SAMPLE_STRENGTH)
    block = build_reasoning(evidence)
    joined = " ".join(block.sentences)
    assert block.available is True
    assert "Đắc lệnh tháng" in block.sentences[0]
    assert "Yếu tố hỗ trợ lực Nhật chủ" in joined
    assert "Đắc lệnh" in joined
    assert "Phân loại lực đã công bố vẫn là Thân vượng." in joined
    assert "Đắc lệnh +4" in joined


def test_impact_describes_consequences_without_advice() -> None:
    """Impact follows the published class and does not recommend."""
    evidence = bind_strength_evidence(SAMPLE_STRENGTH)
    block = build_impact(evidence)
    assert block.available is True
    assert "Thân vượng" in block.sentences[0]
    assert "Ưu tiên" not in block.sentences[0]
    assert "Tránh" not in block.sentences[0]


def test_recommendation_requires_published_useful_god_or_temperature() -> None:
    """No Useful God / Temperature payload means no invented advice."""
    evidence = bind_strength_evidence(SAMPLE_STRENGTH)
    empty = build_recommendation(evidence)
    assert empty.insufficient is True
    filled = build_recommendation(
        evidence,
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    assert filled.available is True
    joined = " ".join(filled.sentences)
    assert "Hỏa · Đinh · Chính Quan" in joined
    assert "Cần ôn" in joined
    assert "Ưu tiên môi trường ấm đã công bố" in joined


def test_summary_synthesizes_prior_blocks_only() -> None:
    """Summary repeats prior first sentences and adds no new facts."""
    unit = compose_strength_narrative(
        SAMPLE_STRENGTH,
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    assert unit.summary.available is True
    text = unit.summary.sentences[0]
    assert "Thân vượng" in text
    assert "Đắc lệnh tháng" in text
    assert "chủ động" in text
    assert "Hỏa · Đinh · Chính Quan" in text
    assert unit.to_dict()["block_order"] == list(STRENGTH_BLOCKS)


def test_compose_publishes_strength_narrative_unit() -> None:
    """Public unit contains evidence and the five speech blocks."""
    unit = compose_strength_narrative(
        SAMPLE_STRENGTH,
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    assert unit.topic_id == "strength"
    assert unit.status == "complete"
    payload = unit.to_dict()
    for key in ("evidence", "observation", "reasoning", "impact", "recommendation", "summary"):
        assert key in payload


def test_empty_strength_payload_is_insufficient() -> None:
    """Missing Strength facts yield honest empty blocks."""
    unit = compose_strength_narrative({})
    assert unit.status == "insufficient"
    assert unit.observation.insufficient is True
    assert unit.summary.insufficient is True
    assert unit.recommendation.insufficient is True


def test_strength_result_object_is_consumed_not_recalculated() -> None:
    """StrengthResult.to_portal_dict is read; calculators are not called."""
    result = StrengthResult(
        success=True,
        strength_level="weak",
        strength_score=0.2,
        season_score=0.1,
        root_score=0.0,
        reasoning="Thiếu căn nên lực mỏng",
    )
    unit = compose_strength_narrative(result)
    assert unit.observation.sentences[0] == "Nhật chủ được đọc là Thân nhược."
    assert unit.evidence.score == 0.2
    assert "Thiếu căn" in unit.reasoning.sentences[0]


def test_strength_narrative_does_not_recalculate_or_open_other_topics() -> None:
    """INT-02B must not import Strength calculators or other topic engines."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in STRENGTH_DIR.glob("*.py"))
    assert "StrengthEngine" not in joined
    assert "StrengthScorer" not in joined
    assert "StrengthAnalyzer" not in joined
    assert "calculators" not in joined
    assert "def calculate(" not in joined
    assert "engines.pattern" not in joined
    assert "engines.luck" not in joined
    assert "engines.shensha" not in joined
    assert "narrative_framework.useful_god" not in joined
    assert "compose_useful_god_narrative" not in joined
    assert "narrative_framework.pattern" not in joined
    assert "compose_pattern_narrative" not in joined
