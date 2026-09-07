"""LANG-08 Marriage Language Pack live integration tests."""

from __future__ import annotations

from pathlib import Path

from consulting.language.bindings.marriage import language_key_for
from consulting.language.catalog import load_validated_marriage_catalog
from consulting.language.versions import FALLBACK_HEADLINE, PLACEHOLDER_TOKEN
from consulting.marriage.language_render import render_marriage_language_cards
from consulting.marriage.report.access import customer_visible_text, expert_visible_text
from tests.consulting.api_fixtures import api_client, valid_body
from tests.consulting.golden.assessment_signature import assessment_signature
from tests.consulting.golden.cases import GOLDEN_CASES, run_golden_case
from tests.consulting.narrative_fixtures import compose_report_bundle

_ROOT = Path(__file__).resolve().parents[2]

_GENERIC = (
    "Trung bình.",
    "Khá hợp.",
    "Rất hợp.",
    "Áp lực cao.",
    "Insufficient.",
    "Có điểm hỗ trợ.",
    "Điểm hỗ trợ nền tảng",
    "__PRODUCT_OWNER_WORDING_REQUIRED__",
)
_FILE_BY_QUESTION = {
    "Q1": "compatibility.yaml",
    "Q2": "support.yaml",
    "Q3": "personality.yaml",
    "Q4": "stability.yaml",
    "Q5": "children.yaml",
    "Q6": "overall.yaml",
}


def test_six_catalog_files_render_live_cards() -> None:
    """Each Assessment question uses its Marriage YAML catalog."""
    decision, payload, _, report = compose_report_bundle()
    assert decision.assessment is not None
    assert len(payload.language_cards) == 6
    for card, language in zip(decision.assessment.cards, payload.language_cards, strict=True):
        expected_key = language_key_for(card.question_id, card.semantic_key)
        assert language.language_key == expected_key
        assert language.language_key.startswith(f"marriage.{card.question_id.lower()}.")
        assert language.headline
        assert language.meaning
        assert PLACEHOLDER_TOKEN not in language.headline
        assert PLACEHOLDER_TOKEN not in language.meaning
    exec_section = next(item for item in report.sections if item.section_id == "executive_summary")
    kinds = {block.kind for block in exec_section.blocks}
    assert {"question", "answer", "meaning"} <= kinds
    blob = customer_visible_text(report)
    for phrase in _GENERIC:
        assert phrase not in blob


def test_renderer_is_deterministic() -> None:
    """Same Decision yields the same Language Pack wording twice."""
    first = compose_report_bundle()
    second = compose_report_bundle()
    a = [(item.language_key, item.variant_id, item.headline) for item in first[1].language_cards]
    b = [(item.language_key, item.variant_id, item.headline) for item in second[1].language_cards]
    assert a == b


def test_missing_language_key_uses_controlled_fallback(caplog) -> None:
    """Missing keys log LANGUAGE_KEY_NOT_FOUND and do not crash."""
    decision, _, _, _ = compose_report_bundle()
    assert decision.assessment is not None
    decision.assessment.cards[0].semantic_key = "not_a_real_state"
    with caplog.at_level("WARNING", logger="consulting.language"):
        cards = render_marriage_language_cards(decision)
    assert cards[0].fallback is True
    assert cards[0].headline == FALLBACK_HEADLINE
    assert "LANGUAGE_KEY_NOT_FOUND" in caplog.text


def test_customer_hides_technical_expert_shows_it() -> None:
    """Technical explanation is expert-only."""
    _, payload, _, report = compose_report_bundle()
    assert any(item.technical_explanation for item in payload.language_cards)
    customer = customer_visible_text(report)
    expert = expert_visible_text(report)
    technical = next(item.technical_explanation for item in payload.language_cards if item.technical_explanation)
    assert technical not in customer
    assert technical in expert


def test_supporting_facts_do_not_expose_ids_or_template_keys() -> None:
    """Bound facts are customer sentences, not catalog or evidence identities."""
    _, payload, _, _ = compose_report_bundle()
    blob = " ".join(
        fact for card in payload.language_cards for fact in card.supporting_facts
    )
    assert "useful_god_support" not in blob
    assert "EV-" not in blob
    assert "F-" not in blob
    assert "CF-" not in blob
    assert "source_fact" not in blob


def test_assessment_golden_semantics_unchanged() -> None:
    """Language Pack must not rewrite Assessment Golden answers or keys."""
    import json
    from pathlib import Path

    from consulting.marriage.models.assessment import QUESTION_ORDER

    expected_dir = Path(__file__).resolve().parent / "golden" / "assessment"
    for case in GOLDEN_CASES:
        actual = assessment_signature(run_golden_case(case.case_id)["decision"])
        expected = json.loads((expected_dir / f"{case.case_id}.json").read_text(encoding="utf-8"))
        assert actual == expected
        assert [card["question_id"] for card in actual["cards"]] == list(QUESTION_ORDER)


def test_decision_golden_overall_state_unchanged() -> None:
    """Decision Golden remains mixed with no score."""
    for case in GOLDEN_CASES:
        signature = run_golden_case(case.case_id)["signature"]
        assert signature["overall_state"] == "mixed"
        assert signature["score"] is None
        assert signature["grade"] is None


def test_live_cards_map_to_catalog_files() -> None:
    """Q1–Q6 language keys belong to the six approved YAML files."""
    catalog = load_validated_marriage_catalog()
    assert [item.path for item in catalog.files] == list(_FILE_BY_QUESTION.values())
    _, payload, _, _ = compose_report_bundle()
    for card in payload.language_cards:
        prefix = card.language_key.split(".")[1]
        question_id = prefix.upper()
        assert question_id in _FILE_BY_QUESTION
        assert card.language_key.startswith(f"marriage.{prefix}.")
        assert card.language_key in catalog.entries_by_key


def test_api_serializes_language_pack_not_generic_answers() -> None:
    """Public Assessment cards expose Language Pack wording, not R02 generic answers."""
    client, _ = api_client(live=False)
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert created.status_code == 201
    cards = created.json()["data"]["assessment_cards"]
    assert len(cards) == 6
    blob = str(cards)
    for phrase in _GENERIC:
        assert phrase not in blob
    for card in cards:
        question_id = str(card["question_id"])
        assert card["headline"]
        assert card["meaning"]
        assert card["language_key"].startswith(f"marriage.{question_id.lower()}.")
        assert PLACEHOLDER_TOKEN not in str(card["headline"])
        assert PLACEHOLDER_TOKEN not in str(card["meaning"])


def test_ui_surfaces_render_language_pack_slots() -> None:
    """Portal and isolated host render Question / Headline / Meaning / Closing."""
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
        assert "mc-assessment-card__meaning" in source
        assert "Cơ sở và giới hạn" in source
        assert "Giải thích kỹ thuật" in source
