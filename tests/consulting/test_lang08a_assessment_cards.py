"""LANG-08A customer Assessment Card composer tests."""

from __future__ import annotations

import json
from pathlib import Path

from consulting.language.bindings.marriage import language_key_for
from consulting.language.catalog import load_validated_marriage_catalog
from consulting.language.renderer import pick_customer_meaning
from consulting.language.versions import PLACEHOLDER_TOKEN
from consulting.marriage.card_composer import compose_customer_assessment_cards
from consulting.marriage.report.access import customer_visible_text, expert_visible_text
from tests.consulting.api_fixtures import api_client, valid_body
from tests.consulting.golden.assessment_signature import assessment_signature
from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case
from tests.consulting.narrative_fixtures import compose_report_bundle

_ROOT = Path(__file__).resolve().parents[2]
_GENERIC = ("Trung bình.", "Insufficient.", "Khá hợp.", "Rất hợp.", "Áp lực cao.")
_FILE_BY_QUESTION = {
    "Q1": "compatibility.yaml",
    "Q2": "support.yaml",
    "Q3": "personality.yaml",
    "Q4": "stability.yaml",
    "Q5": "children.yaml",
    "Q6": "overall.yaml",
}
_CUSTOMER_GOLDEN = Path(__file__).resolve().parent / "golden" / "customer_cards"


def _customer_signature(cards) -> list[dict[str, object]]:
    """Freeze language boundary, not Assessment prose."""
    return [
        {
            "question_id": item.question_id,
            "language_key": item.language_key,
            "verdict": item.headline,
            "fact_source_keys": list(item.fact_source_keys),
            "quick_guidance_action_type": item.quick_guidance_action_type,
            "has_guidance": bool(item.quick_guidance),
            "has_meaning": bool(item.meaning),
        }
        for item in cards
    ]


def test_each_question_resolves_from_its_catalog_file() -> None:
    """Q1–Q6 verdicts load from the six approved YAML files."""
    catalog = load_validated_marriage_catalog()
    decision, payload, _, _ = compose_report_bundle()
    assert decision.assessment is not None
    for card, language in zip(decision.assessment.cards, payload.language_cards, strict=True):
        expected = language_key_for(card.question_id, card.semantic_key)
        assert language.language_key == expected
        assert catalog.entries_by_key[language.language_key].headline
        filename = _FILE_BY_QUESTION[card.question_id]
        assert language.language_key.startswith(f"marriage.{card.question_id.lower()}.")
        assert any(item.path == filename for item in catalog.files)


def test_assessment_prose_is_ignored_in_customer_surfaces() -> None:
    """Assessment.answer must not appear in UI, API, or Report customer text."""
    decision, payload, _, report = compose_report_bundle()
    assert decision.assessment is not None
    api_blob = json.dumps(
        [{"verdict": item.headline, "meaning": item.meaning} for item in payload.language_cards],
        ensure_ascii=False,
    )
    report_blob = customer_visible_text(report)
    for card in decision.assessment.cards:
        if card.answer in _GENERIC:
            assert card.answer not in report_blob
            assert card.answer not in api_blob
            assert all(card.answer != item.headline for item in payload.language_cards)


def test_verdict_comes_from_language_pack_canonical_headline() -> None:
    """Customer verdict is catalog headline, not hashed variant score-speak."""
    catalog = load_validated_marriage_catalog()
    _, payload, _, _ = compose_report_bundle()
    q1 = next(item for item in payload.language_cards if item.question_id == "Q1")
    entry = catalog.entries_by_key[q1.language_key]
    assert q1.headline == " ".join(entry.headline.split())
    assert q1.headline != "Độ hòa hợp ở mức trung bình."
    assert q1.headline != "Trung bình."


def test_meaning_is_not_a_restatement_of_verdict() -> None:
    """One meaning block. It must not clone the verdict."""
    catalog = load_validated_marriage_catalog()
    _, payload, _, _ = compose_report_bundle()
    for card in payload.language_cards:
        entry = catalog.entries_by_key[card.language_key]
        assert card.meaning == pick_customer_meaning(entry, card.headline)
        assert card.meaning
        assert card.meaning.casefold() != card.headline.casefold()
        assert PLACEHOLDER_TOKEN not in card.meaning


def test_supporting_facts_are_source_bound() -> None:
    """Every visible fact keeps a catalog source_fact that bound to Decision."""
    _, payload, _, _ = compose_report_bundle()
    for card in payload.language_cards:
        assert len(card.supporting_facts) == len(card.fact_source_keys)
        assert len(card.supporting_facts) <= 4
        blob = " ".join(card.supporting_facts)
        assert "EV-" not in blob
        assert "F-" not in blob
        assert "CF-" not in blob
        assert "useful_god_support" not in blob


def test_quick_guidance_is_recommendation_bound() -> None:
    """Guidance exists only when an existing Recommendation maps and has B05 wording."""
    decision, payload, _, _ = compose_report_bundle()
    rec_ids = {item.recommendation_id for item in decision.recommendations}
    rec_types = {item.action_type.value for item in decision.recommendations}
    for card in payload.language_cards:
        if not card.quick_guidance:
            assert card.quick_guidance_recommendation_id == ""
            continue
        assert card.quick_guidance.startswith("Gợi ý:")
        assert "reduce_conflict" not in card.quick_guidance
        assert card.quick_guidance_recommendation_id in rec_ids
        assert card.quick_guidance_action_type in rec_types


def test_no_recommendation_means_no_quick_guidance() -> None:
    """Composer must not invent guidance when Recommendation is empty."""
    decision, _, _, _ = compose_report_bundle()
    decision.recommendations = []
    cards = compose_customer_assessment_cards(decision)
    assert all(not item.quick_guidance for item in cards)


def test_q5_never_displays_raw_insufficient() -> None:
    """Children card uses approved Vietnamese insufficient wording."""
    _, payload, _, report = compose_report_bundle()
    q5 = next(item for item in payload.language_cards if item.question_id == "Q5")
    assert q5.language_key == "marriage.q5.insufficient"
    assert "Insufficient" not in q5.headline
    assert "Insufficient" not in q5.meaning
    assert "Insufficient" not in customer_visible_text(report)


def test_customer_hides_technical_expert_shows_it() -> None:
    """Technical explanation stays collapsible expert-only."""
    _, payload, _, report = compose_report_bundle()
    technical = next(item.technical_explanation for item in payload.language_cards if item.technical_explanation)
    assert technical not in customer_visible_text(report)
    assert technical in expert_visible_text(report)


def test_api_ui_report_verdict_parity() -> None:
    """API, Report, and composer share the same verdict/meaning/facts/guidance."""
    _, payload, _, report = compose_report_bundle()
    exec_section = next(item for item in report.sections if item.section_id == "executive_summary")
    for language in payload.language_cards:
        prefix = language.question_id.lower()
        answer = next(item for item in exec_section.blocks if item.block_id == f"{prefix}-answer")
        meaning = next(item for item in exec_section.blocks if item.block_id == f"{prefix}-meaning")
        assert language.headline == answer.body
        assert language.meaning == meaning.body
        guidance = next(
            (item for item in exec_section.blocks if item.block_id == f"{prefix}-guidance"),
            None,
        )
        if language.quick_guidance:
            assert guidance is not None
            assert guidance.body == language.quick_guidance
    client, _ = api_client(live=False)
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert created.status_code == 201
    api_cards = created.json()["data"]["assessment_cards"]
    assert len(api_cards) == 6
    blob = json.dumps(api_cards, ensure_ascii=False)
    for phrase in _GENERIC:
        assert phrase not in blob
    for api in api_cards:
        assert api["verdict"]
        assert api["semantic_key"].startswith("marriage.")
        assert api["verdict"] == api["answer"]
        assert "Insufficient" not in api["verdict"]


def test_composer_is_deterministic() -> None:
    """Same Decision/Assessment/Recommendation yields the same customer cards."""
    first = _customer_signature(compose_report_bundle()[1].language_cards)
    second = _customer_signature(compose_report_bundle()[1].language_cards)
    assert first == second


def test_decision_and_assessment_golden_unchanged() -> None:
    """LANG-08A must not rewrite Decision or Assessment semantic Golden."""
    expected_dir = Path(__file__).resolve().parent / "golden" / "assessment"
    for case in GOLDEN_CASES:
        packed = run_golden_case(case.case_id)
        assert packed["signature"]["overall_state"] == "mixed"
        assert packed["signature"]["score"] is None
        actual = assessment_signature(packed["decision"])
        expected = json.loads((expected_dir / f"{case.case_id}.json").read_text(encoding="utf-8"))
        assert actual == expected


def test_customer_card_golden_freezes_language_boundary() -> None:
    """Customer Card Golden freezes keys, verdict, fact sources, and guidance intent."""
    for case in GOLDEN_CASES:
        packed = run_golden_case(case.case_id)
        cards = compose_customer_assessment_cards(packed["decision"])
        actual = _customer_signature(cards)
        path = _CUSTOMER_GOLDEN / f"{case.case_id}.json"
        expected = json.loads(path.read_text(encoding="utf-8"))
        assert actual == expected


def test_ui_does_not_render_assessment_answer_field() -> None:
    """Portal cards show Language Pack verdict slots, not Assessment.answer."""
    portal = (
        _ROOT
        / "applications"
        / "customer_portal"
        / "src"
        / "features"
        / "marriage_consulting"
        / "ResultView.tsx"
    ).read_text(encoding="utf-8")
    host = (
        _ROOT / "consulting" / "marriage" / "ui" / "static" / "marriage_consulting.js"
    ).read_text(encoding="utf-8")
    for source in (portal, host):
        assert "mc-assessment-card__verdict" in source
        assert "Chi tiết" in source
        assert "Cơ sở" in source
        assert "Gợi ý" in source or "quick_guidance" in source or "quickGuidance" in source
