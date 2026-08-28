"""INT-02B.1 Strength evidence classification tests."""

from __future__ import annotations

from pathlib import Path

from engines.narrative_framework.evidence_item import (
    CLASSIFICATION_NEGATIVE,
    CLASSIFICATION_NEUTRAL,
    CLASSIFICATION_POSITIVE,
    NarrativeEvidenceItem,
)
from engines.narrative_framework.strength import (
    bind_strength_evidence,
    build_observation,
    build_reasoning,
    build_recommendation,
    classify_strength_evidence,
    compose_strength_narrative,
)
from engines.narrative_framework.strength.classify import apply_temperature_strength_effect

STRENGTH_DIR = Path(__file__).resolve().parents[2] / "engines" / "narrative_framework" / "strength"
FRAMEWORK_DIR = STRENGTH_DIR.parent


def _pack(strength: dict, temperature: dict | None = None):
    return classify_strength_evidence(bind_strength_evidence(strength, temperature=temperature))


def test_a_season_positive_evidence() -> None:
    pack = _pack(
        {
            "season_score": 0.35,
            "evidence_compact": "Đắc lệnh +4",
            "strength_level": "strong",
        }
    )
    item = pack.item("season")
    assert item is not None
    assert item.classification == CLASSIFICATION_POSITIVE
    assert item.reason == "Đắc lệnh"
    assert item.source_path == "strength.season_score"


def test_b_season_negative_evidence() -> None:
    pack = _pack({"season_score": -0.25, "evidence_compact": "Tử khí theo tháng"})
    item = pack.item("season")
    assert item is not None
    assert item.classification == CLASSIFICATION_NEGATIVE
    assert item.reason == "Tử"


def test_c_root_positive_evidence() -> None:
    pack = _pack({"root_score": 0.22, "evidence_compact": "Thông căn +3"})
    item = pack.item("root")
    assert item is not None
    assert item.classification == CLASSIFICATION_POSITIVE
    assert item.reason == "Thông căn"


def test_d_support_positive_evidence() -> None:
    pack = _pack({"support_score": 0.1, "reasoning": "Ấn tinh sinh thân"})
    item = pack.item("support")
    assert item is not None
    assert item.classification == CLASSIFICATION_POSITIVE
    assert item.reason == "Ấn tinh"


def test_e_control_negative_evidence() -> None:
    pack = _pack(
        {
            "control_score": -0.1,
            "evidence_compact": "Quan Sát khắc Nhật chủ",
        }
    )
    item = pack.item("control")
    assert item is not None
    assert item.classification == CLASSIFICATION_NEGATIVE
    assert "Quan Sát" in item.reason


def test_f_drain_negative_evidence() -> None:
    pack = _pack({"drain_score": -0.08, "evidence_compact": "Thực Thương tiết khí"})
    item = pack.item("drain")
    assert item is not None
    assert item.classification == CLASSIFICATION_NEGATIVE
    assert "tiết" in item.reason


def test_g_zero_contribution_is_neutral() -> None:
    pack = _pack({"support_score": 0, "control_score": 0, "drain_score": 0})
    assert pack.item("support").classification == CLASSIFICATION_NEUTRAL
    assert pack.item("control").classification == CLASSIFICATION_NEUTRAL
    assert pack.item("drain").classification == CLASSIFICATION_NEUTRAL


def test_h_unavailable_evidence_is_neutral() -> None:
    pack = _pack({})
    season = pack.item("season")
    assert season is not None
    assert season.classification == CLASSIFICATION_NEUTRAL
    assert season.reason == "Chưa có dữ liệu"


def test_i_temperature_does_not_automatically_become_good_or_bad() -> None:
    pack = _pack({"strength_level": "strong"}, temperature={"climate_state_label": "Hàn"})
    item = pack.item("temperature")
    assert item is not None
    assert item.display_value == "Hàn"
    assert item.classification == CLASSIFICATION_NEUTRAL
    explicit = apply_temperature_strength_effect(
        pack,
        {"climate_state_label": "Hàn", "strength_effect": "positive"},
    )
    assert explicit.item("temperature").classification == CLASSIFICATION_POSITIVE
    assert explicit.item("temperature").display_value == "Hàn"


def test_j_special_rule_uses_published_effect_only() -> None:
    pack = _pack(
        {
            "metadata": {
                "trace": {
                    "analysis": {
                        "special_matches": [
                            {
                                "rule_id": "spc_003",
                                "score": -15,
                                "reason": "Thất Sát vô căn",
                            }
                        ]
                    }
                }
            }
        }
    )
    specials = [item for item in pack.evidence_items if item.component == "special_rules"]
    assert specials[0].classification == CLASSIFICATION_NEGATIVE
    assert specials[0].reason == "Thất Sát vô căn"
    assert "special_matches" in specials[0].source_path


def test_k_missing_special_rule_effect_is_neutral() -> None:
    pack = _pack({"metadata": {"trace": {"analysis": {"special_matches": ["spc_001"]}}}})
    specials = [item for item in pack.evidence_items if item.component == "special_rules"]
    assert specials[0].classification == CLASSIFICATION_NEUTRAL
    assert specials[0].reason == "Chưa có dữ liệu"


def test_l_m_source_path_and_reason_preserved() -> None:
    pack = _pack({"season_score": 0.4, "evidence_compact": "Đắc lệnh +4"})
    item = pack.item("season")
    assert item.source_path == "strength.season_score"
    assert item.reason == "Đắc lệnh"


def test_n_o_classification_does_not_change_published_class_or_score() -> None:
    strength = {
        "strength_level": "strong",
        "strength_score": 0.87,
        "confidence": 0.8,
        "season_score": -0.25,
        "control_score": -0.1,
    }
    unit = compose_strength_narrative(strength)
    assert unit.evidence.strength_level == "strong"
    assert unit.evidence.score == 0.87
    assert unit.evidence.confidence == 0.8
    assert unit.observation.sentences[0] == "Nhật chủ được đọc là Thân vượng."


def test_p_observation_consumes_classification() -> None:
    pack = _pack({"strength_level": "weak", "strength_score": 0.2})
    block = build_observation(pack)
    level = pack.item("strength_level")
    assert level is not None
    assert level.display_value == "Thân nhược"
    assert block.sentences[0] == f"Nhật chủ được đọc là {level.display_value}."
    assert block.source_paths[0] == level.source_path


def test_q_reasoning_consumes_grouped_evidence() -> None:
    pack = _pack(
        {
            "strength_level": "strong",
            "season_score": 0.4,
            "root_score": 0.3,
            "control_score": -0.1,
            "drain_score": -0.05,
            "evidence_compact": "Đắc lệnh +4 · Thông căn +3 · Quan Sát -10",
        }
    )
    block = build_reasoning(pack)
    joined = " ".join(block.sentences)
    assert "Yếu tố hỗ trợ lực Nhật chủ" in joined
    assert "Yếu tố suy giảm lực Nhật chủ" in joined
    assert "Phân loại lực đã công bố vẫn là Thân vượng." in joined
    assert pack.positive_evidence
    assert pack.negative_evidence


def test_r_recommendation_remains_independent_of_classification() -> None:
    useful = {"useful_display": "Hỏa · Đinh · Chính Quan"}
    temp = {"balancing_need_label": "Cần ôn"}
    supporting = bind_strength_evidence({"season_score": 0.4, "strength_level": "strong"})
    restraining = bind_strength_evidence({"season_score": -0.4, "strength_level": "strong"})
    left = build_recommendation(supporting, useful_god=useful, temperature=temp)
    right = build_recommendation(restraining, useful_god=useful, temperature=temp)
    assert left.sentences == right.sentences
    assert "Hỏa · Đinh · Chính Quan" in left.sentences[0]


def test_s_summary_introduces_no_new_facts() -> None:
    unit = compose_strength_narrative(
        {
            "strength_level": "strong",
            "strength_score": 0.87,
            "season_score": 0.4,
            "reasoning": "Đắc lệnh tháng",
            "evidence_compact": "Đắc lệnh +4",
        },
        useful_god={"useful_display": "Hỏa"},
    )
    prior = " ".join(
        unit.observation.sentences
        + unit.reasoning.sentences
        + unit.impact.sentences
        + unit.recommendation.sentences
    )
    for sentence in unit.summary.sentences:
        assert sentence in prior or all(
            fragment.strip() in prior for fragment in sentence.rstrip(".").split(". ") if fragment.strip()
        )


def test_t_no_calculator_imports() -> None:
    joined = "\n".join(path.read_text(encoding="utf-8") for path in STRENGTH_DIR.glob("*.py"))
    joined += "\n" + (FRAMEWORK_DIR / "evidence_item.py").read_text(encoding="utf-8")
    assert "StrengthEngine" not in joined
    assert "StrengthScorer" not in joined
    assert "calculators" not in joined
    assert "def calculate(" not in joined
    assert "good_score" not in joined
    assert "auspicious_score" not in joined
    assert isinstance(NarrativeEvidenceItem, type)


def test_item_contract_fields() -> None:
    pack = _pack({"season_score": 0.1, "evidence_compact": "Đắc lệnh"})
    item = pack.item("season")
    payload = item.to_dict()
    for key in (
        "id",
        "topic",
        "component",
        "value",
        "display_value",
        "classification",
        "reason",
        "source_path",
        "confidence",
        "metadata",
    ):
        assert key in payload
    dumped = pack.to_dict()
    assert "raw_evidence" in dumped
    assert dumped["positive_evidence"][0]["id"] == item.id
