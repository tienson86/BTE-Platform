"""INT-02D Pattern Narrative tests. No Pattern Engine execution."""

from __future__ import annotations

from pathlib import Path

from engines.narrative_framework.contracts import BLOCK_TITLES_VI, INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
)
from engines.narrative_framework.pattern import (
    PATTERN_BLOCKS,
    bind_pattern_evidence,
    build_impact,
    build_observation,
    build_reasoning,
    build_recommendation,
    classify_pattern_evidence,
    compose_pattern_narrative,
)
from engines.pattern_engine.engine import PatternResult

TOPIC_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_framework" / "pattern"

SAMPLE_PATTERN = {
    "pattern": "chinh_quan",
    "cach_cuc": "Chính Quan",
    "pattern_quality": "thành cách",
    "follow_type": "",
    "dieu_hau": "Cần ôn",
    "detected_special_pattern": "khuc_truc",
    "winning_rule_id": "PAT-CQ-01",
    "matched_rules": ["PAT-CQ-01", "PAT-CQ-02"],
    "reason": "Tháng lệnh Chính Quan nên lập cách Chính Quan",
    "success_reason": "Tháng lệnh Chính Quan",
    "confidence": 0.84,
    "evidence_compact": "Tháng Dần · Chính Quan xuyên",
    "clash_status": "xung phá nhẹ",
    "combination_status": "hợp cục",
    "dung_than": "Hỏa",
    "hy_than": "Thổ",
    "ky_than": "Kim",
    "recommendations": ["Giữ trục Chính Quan đã công bố"],
}

SAMPLE_USEFUL_GOD = {
    "useful_display": "Hỏa · Đinh · Chính Quan",
    "favorable_display": "Thổ",
}

SAMPLE_TEMPERATURE = {
    "climate_state_label": "Hàn",
    "balancing_need_label": "Cần ôn",
    "recommendations": ["Ưu tiên môi trường ấm đã công bố"],
}


def _pack(payload: dict, temperature: dict | None = None):
    return classify_pattern_evidence(bind_pattern_evidence(payload, temperature=temperature))


def test_evidence_copies_published_pattern_fields() -> None:
    """Evidence is a copy of Pattern output, not a rescore."""
    evidence = bind_pattern_evidence(SAMPLE_PATTERN, temperature=SAMPLE_TEMPERATURE)
    assert evidence.pattern_name == "Chính Quan"
    assert evidence.pattern_class == "thành cách"
    assert evidence.dieu_hau == "Cần ôn"
    assert evidence.special_pattern == "khuc_truc"
    assert evidence.winning_rule == "PAT-CQ-01"
    assert evidence.matched_rules == ("PAT-CQ-01", "PAT-CQ-02")
    assert evidence.confidence == 0.84
    assert evidence.temperature_state == "Hàn"
    assert "pattern_name" not in evidence.missing


def test_observation_states_pattern_dieu_hau_and_special() -> None:
    """Observation names published Pattern facts. It does not advise."""
    block = build_observation(bind_pattern_evidence(SAMPLE_PATTERN))
    assert block.available is True
    assert block.sentences[0] == "Cách cục đã công bố là Chính Quan."
    assert block.sentences[1] == "Điều hậu đã công bố là Cần ôn."
    assert block.sentences[2] == "Cấu trúc đặc biệt đã công bố là khuc_truc."
    joined = " ".join(block.sentences)
    assert "Ưu tiên" not in joined
    assert "Kết luận" not in joined


def test_reasoning_explains_published_and_grouped_evidence() -> None:
    """Reasoning restates published reasoning and grouped classified evidence."""
    block = build_reasoning(bind_pattern_evidence(SAMPLE_PATTERN))
    joined = " ".join(block.sentences)
    assert block.available is True
    assert "Tháng lệnh Chính Quan nên lập cách" in block.sentences[0]
    assert "Yếu tố hỗ trợ cách cục" in joined
    assert "Yếu tố bất lợi cho cách cục" in joined
    assert "Cách cục đã công bố vẫn là Chính Quan." in joined
    assert "Tháng Dần · Chính Quan xuyên" in joined


def test_impact_follows_published_pattern_without_advice() -> None:
    """Impact follows the published Pattern and does not recommend."""
    block = build_impact(bind_pattern_evidence(SAMPLE_PATTERN))
    assert block.available is True
    assert "Chính Quan" in block.sentences[0]
    assert "Ưu tiên" not in block.sentences[0]
    assert "Tránh" not in block.sentences[0]


def test_recommendation_requires_published_guidance() -> None:
    """No published Pattern / Useful God / Temperature guidance means insufficient."""
    empty = build_recommendation(bind_pattern_evidence({"cach_cuc": "Chính Quan"}))
    assert empty.insufficient is True
    assert empty.to_dict()["empty_copy"] == INSUFFICIENT_COPY
    filled = build_recommendation(
        bind_pattern_evidence(SAMPLE_PATTERN),
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    joined = " ".join(filled.sentences)
    assert filled.available is True
    assert "Hỏa · Đinh · Chính Quan" in joined
    assert "Cần ôn" in joined
    assert "Giữ trục Chính Quan đã công bố" in joined


def test_recommendation_does_not_read_classification_buckets() -> None:
    """Polarity grouping cannot invent recommendation text."""
    left = bind_pattern_evidence(SAMPLE_PATTERN)
    stripped = dict(SAMPLE_PATTERN)
    stripped["clash_status"] = ""
    stripped["failure_reason"] = "phá cách"
    right = bind_pattern_evidence(stripped)
    assert build_recommendation(left).sentences == build_recommendation(right).sentences


def test_summary_synthesizes_prior_blocks_only() -> None:
    """Summary repeats prior first sentences and adds no new facts."""
    unit = compose_pattern_narrative(
        SAMPLE_PATTERN,
        useful_god=SAMPLE_USEFUL_GOD,
        temperature=SAMPLE_TEMPERATURE,
    )
    assert unit.summary.available is True
    text = unit.summary.sentences[0]
    assert "Chính Quan" in text
    assert "Tháng lệnh Chính Quan nên lập cách" in text
    assert "trục" in text
    assert "Ưu tiên hướng Dụng thần đã công bố" in text
    assert unit.to_dict()["block_order"] == list(PATTERN_BLOCKS)
    prior = " ".join(
        unit.observation.sentences
        + unit.reasoning.sentences
        + unit.impact.sentences
        + unit.recommendation.sentences
    )
    for fragment in text.rstrip(".").split(". "):
        assert fragment.strip() in prior


def test_compose_publishes_pattern_narrative_unit() -> None:
    """Public unit contains evidence and the five speech blocks."""
    unit = compose_pattern_narrative(SAMPLE_PATTERN)
    assert unit.topic_id == "pattern"
    assert unit.status == "complete"
    payload = unit.to_dict()
    for key in ("evidence", "observation", "reasoning", "impact", "recommendation", "summary"):
        assert key in payload
    assert payload["observation"]["title"] == BLOCK_TITLES_VI["observation"]
    assert payload["evidence_pack"]["raw_evidence"]["pattern_name"] == "Chính Quan"


def test_empty_pattern_payload_is_insufficient() -> None:
    """Missing Pattern facts yield honest empty blocks."""
    unit = compose_pattern_narrative({})
    assert unit.status == "insufficient"
    assert unit.observation.insufficient is True
    assert unit.summary.insufficient is True
    assert unit.recommendation.insufficient is True
    assert unit.recommendation.to_dict()["empty_copy"] == INSUFFICIENT_COPY


def test_pattern_result_object_is_consumed_not_recalculated() -> None:
    """PatternResult.to_portal_dict is read; calculators are not called."""
    result = PatternResult(
        success=True,
        pattern="chinh_quan",
        cach_cuc="Chính Quan",
        reason="Tháng lệnh Chính Quan",
        confidence=0.7,
        dieu_hau="Cần ôn",
        matched_rules=["PAT-CQ-01"],
    )
    unit = compose_pattern_narrative(result)
    assert unit.observation.sentences[0] == "Cách cục đã công bố là Chính Quan."
    assert unit.evidence.pattern_class == "chinh_quan"
    assert "Tháng lệnh Chính Quan" in unit.reasoning.sentences[0]
    assert unit.evidence.matched_rules == ("PAT-CQ-01",)


def test_winning_rule_positive_clash_negative() -> None:
    """Classification is relative to the published Pattern, not fortune."""
    pack = _pack(SAMPLE_PATTERN)
    winning = pack.item("winning_rule")
    clash = pack.item("clash_status")
    assert winning is not None
    assert clash is not None
    assert winning.classification == CLASSIFICATION_POSITIVE
    assert winning.source_path == "pattern.winning_rule_id"
    assert clash.classification == CLASSIFICATION_NEGATIVE
    assert clash.source_path == "pattern.clash_status"


def test_missing_rules_are_neutral_temperature_not_good_or_bad() -> None:
    """Unpublished rules stay neutral; climate state is not collapsed to good/bad."""
    pack = _pack({"cach_cuc": "Chính Quan"}, temperature={"climate_state_label": "Hàn"})
    assert pack.item("matched_rules").classification == CLASSIFICATION_NEUTRAL
    assert pack.item("matched_rules").reason == INSUFFICIENT_COPY
    climate = pack.item("temperature")
    assert climate.display_value == "Hàn"
    assert climate.classification == CLASSIFICATION_NEUTRAL


def test_classification_does_not_change_published_pattern() -> None:
    """Evidence classification cannot rewrite the published determination."""
    payload = dict(SAMPLE_PATTERN)
    payload["failure_reason"] = "xung phá"
    payload["clash_status"] = "xung"
    unit = compose_pattern_narrative(payload)
    assert unit.evidence.pattern_name == "Chính Quan"
    assert unit.observation.sentences[0] == "Cách cục đã công bố là Chính Quan."


def test_observation_and_reasoning_consume_classified_evidence() -> None:
    """Builders read classified items rather than inventing a second Pattern."""
    pack = _pack(SAMPLE_PATTERN)
    observation = build_observation(pack)
    target = pack.item("pattern")
    assert target is not None
    assert observation.sentences[0] == f"Cách cục đã công bố là {target.display_value}."
    reasoning = build_reasoning(pack)
    joined = " ".join(reasoning.sentences)
    assert pack.positive_evidence
    assert pack.negative_evidence
    assert "Yếu tố hỗ trợ cách cục" in joined
    assert "Yếu tố bất lợi cho cách cục" in joined


def test_pattern_narrative_does_not_recalculate_or_import_other_topics() -> None:
    """INT-02D must not import Pattern calculators or sibling topic packages."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in TOPIC_DIR.glob("*.py"))
    assert "PatternEngine" not in joined
    assert "PatternService" not in joined
    assert "calculators" not in joined
    assert "def calculate(" not in joined
    assert "engines.strength" not in joined
    assert "engines.useful_god" not in joined
    assert "narrative_framework.strength" not in joined
    assert "narrative_framework.useful_god" not in joined
    assert "engines.luck" not in joined
    assert "good_score" not in joined
    assert "auspicious_score" not in joined
    assert "narrative_framework.luck" not in joined
    assert "compose_luck_narrative" not in joined
