"""INT-02C Useful God Narrative tests. No Useful God Engine execution."""

from __future__ import annotations

from pathlib import Path

from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
)
from engines.narrative_framework.useful_god import (
    USEFUL_GOD_BLOCKS,
    bind_useful_god_evidence,
    build_impact,
    build_observation,
    build_reasoning,
    build_recommendation,
    classify_useful_god_evidence,
    compose_useful_god_narrative,
)
from engines.useful_god_engine.models import UsefulGodResult

TOPIC_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_framework" / "useful_god"
STRENGTH_DIR = TOPIC_DIR.parent / "strength"

SAMPLE_USEFUL_GOD = {
    "useful_god": "Hỏa",
    "useful_display": "Hỏa · Đinh · Chính Quan",
    "useful_ten_god": "Chính Quan",
    "useful_stem": "Đinh",
    "useful_element": "Hỏa",
    "favorable_gods": ["Thổ"],
    "favorable_display": "Thổ · Mậu · Thiên Ấn",
    "unfavorable_gods": ["Tỷ Kiên", "Kiếp Tài"],
    "unfavorable_display": "Tỷ Kiên · Kiếp Tài",
    "winning_rule_id": "UG-STR-WEAK-01",
    "winning_rule_group": "strength",
    "reasoning": "Thân nhược nên lấy Hỏa Chính Quan làm Dụng thần",
    "confidence": 0.82,
    "matched_rules": ["UG-STR-WEAK-01"],
    "climate_display": "Hỏa",
    "climate_reason": "Cục khí Hàn cần ôn",
    "climate_preference_label": "Cần ôn",
    "recommendations": ["Ưu tiên hướng Hỏa đã công bố"],
    "strength_reason": "Thân nhược cần sinh trợ",
}


def _pack(payload: dict):
    return classify_useful_god_evidence(bind_useful_god_evidence(payload))


def test_evidence_copies_published_useful_god_fields() -> None:
    """Evidence is a copy of Useful God output, not a rescore."""
    evidence = bind_useful_god_evidence(SAMPLE_USEFUL_GOD)
    assert evidence.useful_god == "Hỏa"
    assert evidence.useful_display == "Hỏa · Đinh · Chính Quan"
    assert evidence.useful_ten_god == "Chính Quan"
    assert evidence.favorable_gods == ("Thổ",)
    assert evidence.unfavorable_gods == ("Tỷ Kiên", "Kiếp Tài")
    assert evidence.confidence == 0.82
    assert evidence.winning_rule_id == "UG-STR-WEAK-01"
    assert evidence.recommendations == ("Ưu tiên hướng Hỏa đã công bố",)
    assert "useful_god" not in evidence.missing


def test_observation_names_published_useful_god() -> None:
    """Observation names the published Dụng thần. It does not advise."""
    block = build_observation(bind_useful_god_evidence(SAMPLE_USEFUL_GOD))
    assert block.available is True
    assert block.sentences[0] == "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan."
    assert "Chính Quan" in block.sentences[1]
    joined = " ".join(block.sentences)
    assert "Ưu tiên" not in joined
    assert "Kết luận" not in joined


def test_reasoning_explains_published_and_grouped_evidence() -> None:
    """Reasoning restates published reasoning and grouped classified evidence."""
    block = build_reasoning(bind_useful_god_evidence(SAMPLE_USEFUL_GOD))
    joined = " ".join(block.sentences)
    assert block.available is True
    assert "Thân nhược nên lấy Hỏa Chính Quan" in block.sentences[0]
    assert "Yếu tố hỗ trợ Dụng thần" in joined
    assert "Yếu tố kỵ với Dụng thần" in joined
    assert "Dụng thần đã công bố vẫn là Hỏa · Đinh · Chính Quan." in joined
    assert "Cục khí Hàn cần ôn" in joined


def test_impact_follows_published_useful_god_without_advice() -> None:
    """Impact follows the published Useful God and does not recommend."""
    block = build_impact(bind_useful_god_evidence(SAMPLE_USEFUL_GOD))
    assert block.available is True
    assert "Hỏa · Đinh · Chính Quan" in block.sentences[0]
    assert "Ưu tiên" not in block.sentences[0]
    assert "Tránh" not in block.sentences[0]


def test_recommendation_copies_published_guidance_only() -> None:
    """Recommendation restates published Dụng / Hỷ / Kỵ / climate / recommendations."""
    evidence = bind_useful_god_evidence(SAMPLE_USEFUL_GOD)
    block = build_recommendation(evidence)
    joined = " ".join(block.sentences)
    assert block.available is True
    assert "Hỏa · Đinh · Chính Quan" in joined
    assert "Thổ · Mậu · Thiên Ấn" in joined
    assert "Tỷ Kiên · Kiếp Tài" in joined
    assert "Cần ôn" in joined
    assert "Ưu tiên hướng Hỏa đã công bố" in joined


def test_recommendation_does_not_read_classification_buckets() -> None:
    """Polarity grouping cannot invent recommendation text."""
    supporting = bind_useful_god_evidence(SAMPLE_USEFUL_GOD)
    stripped = dict(SAMPLE_USEFUL_GOD)
    stripped["strength_reason"] = ""
    stripped["matched_rules"] = []
    stripped["winning_rule_id"] = ""
    restraining = bind_useful_god_evidence(stripped)
    assert build_recommendation(supporting).sentences == build_recommendation(restraining).sentences


def test_summary_synthesizes_prior_blocks_only() -> None:
    """Summary repeats prior first sentences and adds no new facts."""
    unit = compose_useful_god_narrative(SAMPLE_USEFUL_GOD)
    assert unit.summary.available is True
    text = unit.summary.sentences[0]
    assert "Hỏa · Đinh · Chính Quan" in text
    assert "Thân nhược nên lấy Hỏa Chính Quan" in text
    assert "trục" in text
    assert "Ưu tiên hướng Dụng thần đã công bố" in text
    assert unit.to_dict()["block_order"] == list(USEFUL_GOD_BLOCKS)
    prior = " ".join(
        unit.observation.sentences
        + unit.reasoning.sentences
        + unit.impact.sentences
        + unit.recommendation.sentences
    )
    for fragment in text.rstrip(".").split(". "):
        assert fragment.strip() in prior


def test_compose_publishes_useful_god_narrative_unit() -> None:
    """Public unit contains evidence and the five speech blocks."""
    unit = compose_useful_god_narrative(SAMPLE_USEFUL_GOD)
    assert unit.topic_id == "useful_god"
    assert unit.status == "complete"
    payload = unit.to_dict()
    for key in ("evidence", "observation", "reasoning", "impact", "recommendation", "summary"):
        assert key in payload
    assert payload["evidence_pack"]["raw_evidence"]["useful_god"] == "Hỏa"


def test_empty_useful_god_payload_is_insufficient() -> None:
    """Missing Useful God facts yield honest empty blocks."""
    unit = compose_useful_god_narrative({})
    assert unit.status == "insufficient"
    assert unit.observation.insufficient is True
    assert unit.summary.insufficient is True
    assert unit.recommendation.insufficient is True


def test_useful_god_result_object_is_consumed_not_recalculated() -> None:
    """UsefulGodResult.to_portal_dict is read; calculators are not called."""
    result = UsefulGodResult(
        success=True,
        useful_god="Hỏa",
        useful_display="Hỏa · Đinh · Chính Quan",
        reasoning="Thân nhược nên lấy Hỏa",
        confidence=0.7,
        recommendations=["Ưu tiên hướng Hỏa đã công bố"],
    )
    unit = compose_useful_god_narrative(result)
    assert unit.observation.sentences[0] == "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan."
    assert unit.evidence.useful_god == "Hỏa"
    assert "Thân nhược nên lấy Hỏa" in unit.reasoning.sentences[0]
    assert unit.evidence.recommendations == ("Ưu tiên hướng Hỏa đã công bố",)


def test_favorable_is_positive_unfavorable_is_negative() -> None:
    """Hỷ supports the published Useful God; Kỵ restrains it. Not fortune labels."""
    pack = _pack(SAMPLE_USEFUL_GOD)
    favorable = pack.item("favorable")
    unfavorable = pack.item("unfavorable")
    assert favorable is not None
    assert unfavorable is not None
    assert favorable.classification == CLASSIFICATION_POSITIVE
    assert favorable.reason == "Thổ · Mậu · Thiên Ấn"
    assert favorable.source_path == "useful_god.favorable_display"
    assert unfavorable.classification == CLASSIFICATION_NEGATIVE
    assert "Kỵ thần" in unfavorable.reason or "Tỷ Kiên" in unfavorable.reason
    assert unfavorable.source_path == "useful_god.unfavorable_display"


def test_missing_and_insufficient_favorable_are_neutral() -> None:
    """Zero / unpublished Hỷ does not fabricate polarity."""
    missing = _pack({"useful_display": "Hỏa"})
    assert missing.item("favorable").classification == CLASSIFICATION_NEUTRAL
    assert missing.item("favorable").reason == "Chưa có dữ liệu"
    overlay = _pack(
        {
            "useful_display": "Hỏa",
            "favorable_display": "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng",
        }
    )
    assert overlay.item("favorable").classification == CLASSIFICATION_NEUTRAL


def test_climate_is_not_automatically_good_or_bad() -> None:
    """Climate Useful God state is preserved and stays neutral unless unpublished."""
    pack = _pack({"useful_display": "Hỏa", "climate_display": "Hàn"})
    climate = pack.item("climate")
    assert climate is not None
    assert climate.display_value == "Hàn"
    assert climate.classification == CLASSIFICATION_NEUTRAL


def test_classification_does_not_change_published_useful_god() -> None:
    """Evidence classification cannot rewrite the published determination."""
    payload = dict(SAMPLE_USEFUL_GOD)
    payload["unfavorable_gods"] = ["Tỷ Kiên", "Kiếp Tài", "Thất Sát"]
    unit = compose_useful_god_narrative(payload)
    assert unit.evidence.useful_god == "Hỏa"
    assert unit.evidence.useful_display == "Hỏa · Đinh · Chính Quan"
    assert unit.observation.sentences[0] == "Dụng thần đã công bố là Hỏa · Đinh · Chính Quan."


def test_observation_and_reasoning_consume_classified_evidence() -> None:
    """Builders read classified items rather than inventing a second determination."""
    pack = _pack(SAMPLE_USEFUL_GOD)
    observation = build_observation(pack)
    target = pack.item("useful_god")
    assert target is not None
    assert observation.sentences[0] == f"Dụng thần đã công bố là {target.display_value}."
    reasoning = build_reasoning(pack)
    joined = " ".join(reasoning.sentences)
    assert pack.positive_evidence
    assert pack.negative_evidence
    assert "Yếu tố hỗ trợ Dụng thần" in joined
    assert "Yếu tố kỵ với Dụng thần" in joined


def test_useful_god_narrative_does_not_recalculate_or_open_other_topics() -> None:
    """INT-02C must not import Useful God calculators or other topic engines."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in TOPIC_DIR.glob("*.py"))
    assert "UsefulGodEngine" not in joined
    assert "StrengthEngine" not in joined
    assert "calculators" not in joined
    assert "def calculate(" not in joined
    assert "engines.pattern" not in joined
    assert "engines.luck" not in joined
    assert "engines.shensha" not in joined
    assert "narrative_framework.strength" not in joined
    assert "good_score" not in joined
    assert "auspicious_score" not in joined
    assert STRENGTH_DIR.exists()
    assert "narrative_framework.pattern" not in joined
    assert "compose_pattern_narrative" not in joined
