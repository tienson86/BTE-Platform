"""R2 Expert Translation Layer tests."""

from __future__ import annotations

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.narrative import (
    compose_narrative_v2,
    compose_narrative_v2_from_production,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_CONCLUSION,
    KIND_REASON,
    SLOT_REASONING,
    SLOT_SUMMARY,
)
from engines.interpretation_engine.foundation.narrative.input import (
    CopiedStatement,
    DecisionBundle,
    NarrativeComposerInput,
)
from engines.interpretation_engine.foundation.narrative.production import (
    build_composer_input_from_production,
)
from engines.interpretation_engine.foundation.narrative.translation import (
    TRANSLATION_SCOPES,
    ExpertTranslationError,
    apply_expert_translation,
    assert_customer_text_clean,
    confidence_label,
    find_forbidden_terms,
    load_translation_rules,
    translate_text,
)
from engines.interpretation_engine.foundation.narrative.translation.validator import (
    customer_narrative_blob,
)

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
)

SON = ProductionRequest(
    year=1987,
    month=1,
    day=21,
    hour=4,
    minute=30,
    gender="male",
    timezone="Asia/Bangkok",
    full_name="Nguyễn Tiến Sơn",
)


def test_translation_rules_cover_required_categories() -> None:
    """Every required translation category has at least one rule."""
    scopes = {rule.scope for rule in load_translation_rules()}
    assert set(TRANSLATION_SCOPES) <= scopes


def test_engine_candidate_load_becomes_expert_language() -> None:
    """Loaded-candidate dumps are translated, not shown."""
    text = translate_text("Loaded 6 candidates from engine")
    assert "Loaded" not in text
    assert "candidates" not in text.casefold()
    assert "Hệ thống đã đánh giá nhiều phương án cân bằng" in text


def test_winner_becomes_best_option() -> None:
    """Winner dumps become expert selection language."""
    text = translate_text("Winner Đinh score 0.85 via sea_004")
    assert "winner" not in text.casefold()
    assert "sea_004" not in text
    assert "0.85" not in text
    assert "Phương án phù hợp nhất" in text
    assert "Đinh" in text


def test_priority_assignment_is_not_exposed() -> None:
    """Numeric priority assignments become expert priority language."""
    text = translate_text("priority=80")
    assert "priority" not in text.casefold()
    assert "80" not in text
    assert "mức độ ưu tiên" in text.casefold()


def test_rejected_candidate_keeps_reference_value() -> None:
    """Rejected options stay useful, without ranking jargon."""
    text = translate_text("Rejected candidate")
    assert "rejected" not in text.casefold()
    assert "vẫn có giá trị tham khảo" in text


def test_confidence_bands_hide_raw_floats() -> None:
    """Unit-interval scores become expert bands."""
    assert confidence_label(0.85).startswith("Mức độ phù hợp cao")
    assert confidence_label(0.55).startswith("Mức độ phù hợp trung bình")
    assert "0.85" not in translate_text("độ tin cậy 0.85")


def test_debug_mode_preserves_engine_language() -> None:
    """Developer/debug mode does not rewrite engine dumps."""
    raw = "Loaded 6 candidates from engine"
    assert translate_text(raw, debug_mode=True) == raw


def test_validator_fails_on_forbidden_engine_language() -> None:
    """Customer-text validation fails closed on engine dumps."""
    with pytest.raises(ExpertTranslationError):
        assert_customer_text_clean("Loaded 6 candidates; winner sea_004")
    assert find_forbidden_terms("Phương án phù hợp nhất là Đinh.") == ()


def test_translation_preserves_decision_and_evidence_refs() -> None:
    """Selected value and engine_truth_ref stay unchanged."""
    source = NarrativeComposerInput(
        decision_bundles=(
            DecisionBundle(
                bundle_id="decision:UsefulGod",
                domain="UsefulGod",
                selected="Đinh",
                reason="Winner Đinh score 0.85 via sea_004",
                confidence=0.85,
                importance=1.0,
                statements=(
                    CopiedStatement(
                        text="Loaded 6 candidates from engine",
                        kind=KIND_REASON,
                        slot=SLOT_REASONING,
                        engine_truth_ref="decision:UsefulGod:path:load_candidates",
                        confidence=0.85,
                    ),
                    CopiedStatement(
                        text="Đinh: selected by seasonal command",
                        kind=KIND_CONCLUSION,
                        slot=SLOT_SUMMARY,
                        engine_truth_ref="decision:UsefulGod:selected",
                        confidence=0.85,
                    ),
                ),
                engine_truth_refs=("decision:UsefulGod:selected",),
            ),
        )
    )
    translated = apply_expert_translation(source)
    bundle = translated.decision_bundles[0]
    assert bundle.selected == "Đinh"
    assert bundle.confidence == 0.85
    assert bundle.bundle_id == "decision:UsefulGod"
    assert bundle.statements[0].engine_truth_ref == (
        "decision:UsefulGod:path:load_candidates"
    )
    assert "Loaded" not in bundle.statements[0].text
    result = compose_narrative_v2(source)
    assert result.metrics.traceability_coverage == 1.0
    assert result.metrics.orphan_sentence_count == 0


def _assert_clean_expert_narrative(output, expected_selected: str) -> None:
    """Shared golden checks: no engine language, same decision, evidence kept."""
    source = build_composer_input_from_production(output)
    selected = {
        bundle.selected for bundle in source.decision_bundles if bundle.selected
    }
    assert expected_selected in selected
    result = compose_narrative_v2_from_production(output)
    blob = customer_narrative_blob(result)
    assert find_forbidden_terms(blob) == ()
    assert "Loaded" not in blob
    assert "sea_004" not in blob
    assert "tmp_003" not in blob
    assert "flo_001" not in blob
    assert expected_selected in blob
    assert result.metrics.traceability_coverage == 1.0
    translated = apply_expert_translation(source)
    after_selected = {
        bundle.selected for bundle in translated.decision_bundles if bundle.selected
    }
    assert selected == after_selected
    assert translated.decision_bundles[0].engine_truth_refs


def test_golden_huynh_expert_translation(huynh_output) -> None:
    """Lương Ngọc Huỳnh customer narrative has expert language, same decision."""
    _assert_clean_expert_narrative(huynh_output, "Chính Tài")


def test_golden_son_expert_translation(son_output) -> None:
    """Nguyễn Tiến Sơn customer narrative has expert language, same decision."""
    selected = son_output.interpretation_foundation.facts.useful_god.selected
    _assert_clean_expert_narrative(son_output, selected)


def test_golden_case_0001_expert_translation(case_0001_output) -> None:
    """CASE-0001 customer narrative has expert language, same decision."""
    selected = case_0001_output.interpretation_foundation.facts.useful_god.selected
    _assert_clean_expert_narrative(case_0001_output, selected)
    assert CASE_0001_REQUEST.full_name == "Nguyễn Tiến Sơn"


@pytest.fixture(scope="module")
def huynh_output():
    """Production pipeline output for Lương Ngọc Huỳnh."""
    return ProductionEngineRunner().run(HUYNH)


@pytest.fixture(scope="module")
def son_output():
    """Production pipeline output for Nguyễn Tiến Sơn."""
    return ProductionEngineRunner().run(SON)


@pytest.fixture(scope="module")
def case_0001_output():
    """Production pipeline output for CASE-0001."""
    return ProductionEngineRunner().run(CASE_0001_REQUEST)
