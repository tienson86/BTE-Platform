"""INT-02E Luck Narrative tests. No Luck Engine execution."""

from __future__ import annotations

from pathlib import Path

from engines.luck_engine.context import LuckContext
from engines.luck_engine.models.periods import DayunPeriod, LiunianPeriod
from engines.narrative_framework.contracts import BLOCK_TITLES_VI, INSUFFICIENT_COPY
from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
)
from engines.narrative_framework.luck import (
    LUCK_BLOCKS,
    bind_luck_evidence,
    build_impact,
    build_observation,
    build_reasoning,
    build_recommendation,
    classify_luck_evidence,
    compose_luck_narrative,
)

TOPIC_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_framework" / "luck"

SAMPLE_LUCK = {
    "current_dayun": {
        "index": 3,
        "start_age": 32,
        "start_year": 2024,
        "ganzhi": "Giáp Thìn",
    },
    "current_liunian": {"year": 2026, "ganzhi": "Bính Ngọ"},
    "timeline": "Đại Vận Giáp Thìn · Lưu Niên Bính Ngọ",
    "luck_stage": "vượng",
    "luck_summary": "Đại Vận Giáp Thìn đang chạy, Lưu Niên Bính Ngọ tiếp nhịp",
    "confidence": 0.81,
    "support_elements": ["Mộc", "Hỏa"],
    "attack_elements": ["Kim"],
    "recommendations": ["Giữ nhịp Đại Vận đã công bố"],
}


def _pack(payload: dict):
    return classify_luck_evidence(bind_luck_evidence(payload))


def test_evidence_copies_published_luck_fields() -> None:
    """Evidence is a copy of Luck output, not a rescore."""
    evidence = bind_luck_evidence(SAMPLE_LUCK)
    assert evidence.current_cycle == "Giáp Thìn"
    assert evidence.current_liunian == "Bính Ngọ"
    assert evidence.cycle_index == 3
    assert evidence.age == 32
    assert evidence.reference_year == 2026
    assert evidence.timeline == "Đại Vận Giáp Thìn · Lưu Niên Bính Ngọ"
    assert evidence.confidence == 0.81
    assert evidence.recommendations == ("Giữ nhịp Đại Vận đã công bố",)
    assert "current_cycle" not in evidence.missing


def test_observation_states_dayun_liunian_and_timeline() -> None:
    """Observation names published Đại Vận, Lưu Niên, and timeline. It does not advise."""
    block = build_observation(bind_luck_evidence(SAMPLE_LUCK))
    assert block.available is True
    assert block.sentences[0] == "Đại Vận hiện tại đã công bố là Giáp Thìn."
    assert block.sentences[1] == "Lưu Niên hiện tại đã công bố là Bính Ngọ."
    assert block.sentences[2] == "Timeline đã công bố là Đại Vận Giáp Thìn · Lưu Niên Bính Ngọ."
    joined = " ".join(block.sentences)
    assert "Ưu tiên" not in joined
    assert "Kết luận" not in joined


def test_reasoning_uses_timeline_and_grouped_evidence() -> None:
    """Reasoning restates published reasoning, timeline, and classified groups."""
    block = build_reasoning(bind_luck_evidence(SAMPLE_LUCK))
    joined = " ".join(block.sentences)
    assert block.available is True
    assert "Đại Vận Giáp Thìn đang chạy" in block.sentences[0]
    assert "Timeline đã công bố" in joined
    assert "Yếu tố hỗ trợ vận đã công bố" in joined
    assert "Yếu tố xung khắc vận đã công bố" in joined
    assert "Giai đoạn vận đã công bố vẫn là vượng." in joined


def test_impact_describes_current_stage_without_prediction() -> None:
    """Impact follows the published stage and does not predict."""
    block = build_impact(bind_luck_evidence(SAMPLE_LUCK))
    assert block.available is True
    assert "vượng" in block.sentences[0]
    assert "Ưu tiên" not in block.sentences[0]
    assert "sẽ" not in block.sentences[0]


def test_recommendation_copies_published_luck_guidance_only() -> None:
    """No published Luck recommendations means insufficient. No invented advice."""
    empty = build_recommendation(bind_luck_evidence({"current_cycle": "Giáp Thìn"}))
    assert empty.insufficient is True
    assert empty.to_dict()["empty_copy"] == INSUFFICIENT_COPY
    filled = build_recommendation(bind_luck_evidence(SAMPLE_LUCK))
    assert filled.available is True
    assert "Giữ nhịp Đại Vận đã công bố" in filled.sentences[0]


def test_recommendation_does_not_read_classification_buckets() -> None:
    """Polarity grouping cannot invent recommendation text."""
    left = bind_luck_evidence(SAMPLE_LUCK)
    stripped = dict(SAMPLE_LUCK)
    stripped["attack_elements"] = ["Kim", "Thổ"]
    stripped["support_elements"] = []
    right = bind_luck_evidence(stripped)
    assert build_recommendation(left).sentences == build_recommendation(right).sentences


def test_summary_synthesizes_prior_blocks_only() -> None:
    """Summary repeats prior first sentences and adds no new facts."""
    unit = compose_luck_narrative(SAMPLE_LUCK)
    assert unit.summary.available is True
    text = unit.summary.sentences[0]
    assert "Giáp Thìn" in text
    assert "Đại Vận Giáp Thìn đang chạy" in text
    assert "trục" in text
    assert "Giữ nhịp Đại Vận đã công bố" in text
    assert unit.to_dict()["block_order"] == list(LUCK_BLOCKS)
    prior = " ".join(
        unit.observation.sentences
        + unit.reasoning.sentences
        + unit.impact.sentences
        + unit.recommendation.sentences
    )
    for fragment in text.rstrip(".").split(". "):
        assert fragment.strip() in prior


def test_compose_publishes_luck_narrative_unit() -> None:
    """Public unit contains evidence and the five speech blocks."""
    unit = compose_luck_narrative(SAMPLE_LUCK)
    assert unit.topic_id == "luck"
    assert unit.status == "complete"
    payload = unit.to_dict()
    for key in ("evidence", "observation", "reasoning", "impact", "recommendation", "summary"):
        assert key in payload
    assert payload["observation"]["title"] == BLOCK_TITLES_VI["observation"]
    assert payload["evidence_pack"]["raw_evidence"]["current_cycle"] == "Giáp Thìn"


def test_empty_luck_payload_is_insufficient() -> None:
    """Missing Luck facts yield honest empty blocks."""
    unit = compose_luck_narrative({})
    assert unit.status == "insufficient"
    assert unit.observation.insufficient is True
    assert unit.summary.insufficient is True
    assert unit.recommendation.insufficient is True
    assert unit.recommendation.to_dict()["empty_copy"] == INSUFFICIENT_COPY


def test_luck_context_object_is_consumed_not_recalculated() -> None:
    """LuckContext.to_dict is read; LuckEngine is not called."""
    result = LuckContext(
        current_dayun=DayunPeriod(
            index=3,
            start_age=32,
            end_age=41,
            start_year=2024,
            end_year=2033,
            heavenly_stem="Giáp",
            earthly_branch="Thìn",
            element="Mộc",
            yin_yang="yang",
            ten_god="Thiên Ấn",
        ),
        current_liunian=LiunianPeriod(
            year=2026,
            ganzhi="Bính Ngọ",
            heavenly_stem="Bính",
            earthly_branch="Ngọ",
            element="Hỏa",
            yin_yang="yang",
            ten_god="Thực Thần",
        ),
        luck_stage="vượng",
        luck_summary="Đại Vận Giáp Thìn đang chạy",
        confidence=0.7,
        available=True,
        reason=None,
        metadata={"recommendations": ["Giữ nhịp Đại Vận đã công bố"]},
    )
    unit = compose_luck_narrative(result)
    assert unit.observation.sentences[0] == "Đại Vận hiện tại đã công bố là Giáp Thìn."
    assert unit.evidence.cycle_index == 3
    assert unit.evidence.reference_year == 2026
    assert "Đại Vận Giáp Thìn đang chạy" in unit.reasoning.sentences[0]
    assert unit.evidence.recommendations == ("Giữ nhịp Đại Vận đã công bố",)


def test_support_is_positive_attack_is_negative() -> None:
    """Classification is relative to published Luck evidence, not fortune."""
    pack = _pack(SAMPLE_LUCK)
    support = pack.item("support")
    attack = pack.item("attack")
    cycle = pack.item("current_cycle")
    assert support is not None
    assert attack is not None
    assert cycle is not None
    assert support.classification == CLASSIFICATION_POSITIVE
    assert "Mộc" in support.reason
    assert support.source_path == "luck.support_elements"
    assert attack.classification == CLASSIFICATION_NEGATIVE
    assert attack.source_path == "luck.attack_elements"
    assert cycle.classification == CLASSIFICATION_NEUTRAL


def test_missing_groups_are_neutral_stage_is_not_fortune() -> None:
    """Unpublished support/attack stay neutral; stage is not collapsed to good/bad."""
    pack = _pack({"current_cycle": "Giáp Thìn", "luck_stage": "vượng"})
    assert pack.item("support").classification == CLASSIFICATION_NEUTRAL
    assert pack.item("support").reason == INSUFFICIENT_COPY
    stage = pack.item("luck_stage")
    assert stage.display_value == "vượng"
    assert stage.classification == CLASSIFICATION_NEUTRAL


def test_classification_does_not_change_published_luck() -> None:
    """Evidence classification cannot rewrite the published Đại Vận / Lưu Niên."""
    payload = dict(SAMPLE_LUCK)
    payload["attack_elements"] = ["Kim", "Thổ", "Thủy"]
    unit = compose_luck_narrative(payload)
    assert unit.evidence.current_cycle == "Giáp Thìn"
    assert unit.evidence.current_liunian == "Bính Ngọ"
    assert unit.observation.sentences[0] == "Đại Vận hiện tại đã công bố là Giáp Thìn."


def test_observation_and_reasoning_consume_classified_evidence() -> None:
    """Builders read classified items rather than inventing a second Luck reading."""
    pack = _pack(SAMPLE_LUCK)
    observation = build_observation(pack)
    cycle = pack.item("current_cycle")
    assert cycle is not None
    assert observation.sentences[0] == f"Đại Vận hiện tại đã công bố là {cycle.display_value}."
    reasoning = build_reasoning(pack)
    joined = " ".join(reasoning.sentences)
    assert pack.positive_evidence
    assert pack.negative_evidence
    assert "Yếu tố hỗ trợ vận đã công bố" in joined
    assert "Yếu tố xung khắc vận đã công bố" in joined


def test_luck_narrative_does_not_recalculate_or_import_other_topics() -> None:
    """INT-02E must not import Luck calculators or sibling topic packages."""
    joined = "\n".join(path.read_text(encoding="utf-8") for path in TOPIC_DIR.glob("*.py"))
    assert "LuckEngine" not in joined
    assert "CanonicalLuckPipeline" not in joined
    assert "calculators" not in joined
    assert "def calculate(" not in joined
    assert "narrative_framework.strength" not in joined
    assert "narrative_framework.useful_god" not in joined
    assert "narrative_framework.pattern" not in joined
    assert "good_score" not in joined
    assert "auspicious_score" not in joined
    assert "opportunity_score" not in joined
