"""TV1-R02 Marriage Assessment projection tests. Decision Golden stays frozen."""

from __future__ import annotations

import json
from pathlib import Path

from consulting.marriage.models.assessment import CUSTOMER_QUESTIONS, QUESTION_ORDER
from consulting.marriage.report.access import customer_visible_text
from tests.consulting.golden.assessment_signature import assessment_signature
from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case
from tests.consulting.narrative_fixtures import compose_report_bundle

_GENERIC_LABELS = (
    "Điểm hỗ trợ nền tảng",
    "Điểm bổ trợ vai trò",
    "Điểm cần lưu ý ở nền tảng",
    "Điểm ma sát Can Chi",
    "Có điểm hỗ trợ.",
)
_ASSESSMENT_DIR = Path(__file__).resolve().parent / "golden" / "assessment"


def test_assessment_has_exactly_six_question_cards() -> None:
    """Public Assessment answers the frozen TV-01 Question Set."""
    decision, _, _, report = compose_report_bundle()
    assert decision.assessment is not None
    cards = decision.assessment.cards
    assert [item.question_id for item in cards] == list(QUESTION_ORDER)
    assert [item.question for item in cards] == [CUSTOMER_QUESTIONS[item] for item in QUESTION_ORDER]
    assert all(item.answer for item in cards)
    assert all(len(item.supporting_facts) <= 4 for item in cards)
    assert all(item.confidence in {"High", "Medium", "Reference"} for item in cards)
    exec_section = next(item for item in report.sections if item.section_id == "executive_summary")
    assert exec_section.title == "Đánh giá hôn nhân"
    questions = [block.body for block in exec_section.blocks if block.kind == "question"]
    assert questions == [CUSTOMER_QUESTIONS[item] for item in QUESTION_ORDER]


def test_assessment_does_not_change_decision_golden() -> None:
    """R02 must not rewrite Decision overall state, score, or evidence."""
    for case in GOLDEN_CASES:
        signature = run_golden_case(case.case_id)["signature"]
        assert signature["score"] is None
        assert signature["grade"] is None
        assert signature["overall_state"] == "mixed"


def test_children_card_does_not_predict_fertility() -> None:
    """Children Assessment never predicts count, gender, or fertility."""
    decision, _, _, _ = compose_report_bundle()
    assert decision.assessment is not None
    children = next(item for item in decision.assessment.cards if item.question_id == "Q5")
    blob = " ".join([children.answer, *children.supporting_facts]).lower()
    assert children.answer.startswith("Insufficient")
    assert "số con" not in blob
    assert "giới tính" not in blob
    assert "fertility" not in blob


def test_assessment_facts_are_concrete() -> None:
    """Supporting facts must not fall back to generic standalone labels."""
    _, _, _, report = compose_report_bundle()
    blob = customer_visible_text(report)
    for phrase in _GENERIC_LABELS:
        assert phrase not in blob
    assert "/100" not in blob
    assert "82%" not in blob


def test_assessment_golden_layer_frozen() -> None:
    """Assessment Golden files freeze Question Logic output. Decision JSON is untouched."""
    for case in GOLDEN_CASES:
        expected_path = _ASSESSMENT_DIR / f"{case.case_id}.json"
        assert expected_path.is_file(), f"missing assessment golden {expected_path}"
        actual = assessment_signature(run_golden_case(case.case_id)["decision"])
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert actual == expected
        assert [card["question_id"] for card in actual["cards"]] == list(QUESTION_ORDER)
        assert actual["cards"][4]["question_id"] == "Q5"
        assert actual["cards"][4]["answer"].startswith("Insufficient")
