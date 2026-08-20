"""CI1 Case Thesis Generator tests A–T."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.narrative import (
    compose_narrative_v2,
    compose_narrative_v2_from_production,
)
from engines.interpretation_engine.foundation.narrative.case_thesis import (
    CROSS_CASE_SIMILARITY_MAX,
    compare_case_theses,
    generate_case_thesis,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_CONCLUSION,
    KIND_FACT,
    KIND_REASON,
    SLOT_CONCLUSION,
    SLOT_OBSERVATION,
    SLOT_REASONING,
    SLOT_SUMMARY,
)
from engines.interpretation_engine.foundation.narrative.input import (
    ChartFocus,
    CopiedStatement,
    DecisionBundle,
    NarrativeComposerInput,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.production import (
    build_composer_input_from_production,
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

_NARRATIVE_ROOT = Path("engines/interpretation_engine/foundation/narrative")
_FORBIDDEN_ENGINE_IMPORTS = (
    "from engines.calendar_engine",
    "from engines.bazi_engine",
    "from engines.score_engine",
    "from engines.pattern_engine",
    "from engines.useful_god",
    "from engines.ten_gods_engine",
)
_FORBIDDEN_UI_IMPORTS = (
    "applications.customer_portal",
    "engines.report_engine.commercial.builder",
    "from engines.narrative_engine",
)
_PERSON_NAMES = ("Nguyễn Tiến Sơn", "Ngô Đặng Minh Tân", "Lương Ngọc Huỳnh", "CASE-0001")


@pytest.fixture(scope="module")
def son_output():
    """Production pipeline output for CASE-0001."""
    return ProductionEngineRunner().run(CASE_0001_REQUEST)


@pytest.fixture(scope="module")
def huynh_output():
    """Production pipeline output for Lương Ngọc Huỳnh."""
    return ProductionEngineRunner().run(HUYNH)


def _tan_focus() -> ChartFocus:
    """Current visible analytical truth for Ngô Đặng Minh Tân. Not a birth fixture."""
    return ChartFocus(
        selected="Canh",
        favorable=("Canh", "Tân", "Nhâm"),
        unfavorable=("Giáp", "Ất"),
        pattern_label="Chính Ấn",
        strength_label="Trung hòa",
        strength_state="balanced",
        day_master="Bính",
        present_ten_gods=("Chính Ấn", "Canh", "Giáp", "Ất"),
        canonical_shensha=("Hồng Loan", "Hoa Cái"),
        current_dayun="Đinh Tỵ 2024–2033",
        five_elements=(
            ("Mộc", 6),
            ("Hỏa", 1),
            ("Thổ", 3),
            ("Kim", 1),
            ("Thủy", 3),
        ),
        dominant_element="Mộc",
        stem_roles=(("Canh", "Chính Tài"), ("Giáp", "Chính Ấn"), ("Ất", "Thiên Ấn")),
    )


def _input_from_focus(focus: ChartFocus) -> NarrativeComposerInput:
    """Minimal governing bundles copied from a ChartFocus. No engine run."""
    return NarrativeComposerInput(
        decision_bundles=(
            DecisionBundle(
                bundle_id="decision:UsefulGod",
                domain="UsefulGod",
                selected=focus.selected,
                reason=f"Đã chọn {focus.selected}",
                confidence=0.9,
                importance=1.0,
                statements=(
                    CopiedStatement(
                        text=f"Dụng thần hiện tại là {focus.selected}.",
                        kind=KIND_CONCLUSION,
                        slot=SLOT_SUMMARY,
                        engine_truth_ref="useful_god:selected",
                        confidence=0.9,
                    ),
                    CopiedStatement(
                        text=f"Hướng chỉnh lấy {focus.selected} làm trục.",
                        kind=KIND_REASON,
                        slot=SLOT_REASONING,
                        engine_truth_ref="useful_god:reason",
                        confidence=0.9,
                    ),
                    CopiedStatement(
                        text=f"Nhật chủ {focus.day_master}.",
                        kind=KIND_FACT,
                        slot=SLOT_OBSERVATION,
                        engine_truth_ref="bazi:day_master",
                        confidence=0.9,
                    ),
                ),
                engine_truth_refs=("useful_god:selected",),
            ),
        ),
        state_bundles=(
            StateBundle(
                bundle_id="state:Strength",
                domain="Strength",
                state=focus.strength_state,
                label=focus.strength_label,
                confidence=0.9,
                importance=0.85,
                statements=(
                    CopiedStatement(
                        text=focus.strength_label or focus.strength_state,
                        kind=KIND_FACT,
                        slot=SLOT_OBSERVATION,
                        engine_truth_ref="strength:label",
                        confidence=0.9,
                    ),
                ),
                engine_truth_refs=("strength:label",),
            ),
        ),
        relationship_bundles=(),
        knowledge_bundles=(),
        chart_focus=focus,
    )


def test_a_thesis_builds_from_current_domain_bundles(son_output) -> None:
    """A. Thesis builds from current domain bundles."""
    source = build_composer_input_from_production(son_output)
    thesis = generate_case_thesis(source)
    assert thesis.status == "complete"
    assert source.chart_focus is not None
    assert thesis.core_pattern == source.chart_focus.pattern_label
    assert thesis.supporting_domains
    assert "UsefulGod" in thesis.supporting_domains or source.decision_bundles


def test_b_thesis_never_alters_engine_truth(son_output) -> None:
    """B. Thesis never alters engine truth."""
    foundation = son_output.interpretation_foundation
    source = build_composer_input_from_production(son_output)
    before = (
        foundation.useful_god_explanation.decision.selected,
        foundation.facts.strength.level,
        foundation.facts.pattern.label,
    )
    compose_narrative_v2_from_production(son_output)
    after = (
        foundation.useful_god_explanation.decision.selected,
        foundation.facts.strength.level,
        foundation.facts.pattern.label,
    )
    assert before == after
    assert source.decision_bundles[0].selected == before[0]


def test_c_thesis_has_evidence_coverage_1(son_output) -> None:
    """C. Thesis has evidence coverage 1.0."""
    result = compose_narrative_v2_from_production(son_output)
    assert result.case_thesis is not None
    assert result.case_thesis.thesis_evidence_coverage == 1.0
    assert result.case_thesis.evidence_ids
    assert result.case_thesis.unsupported_thesis_claims == 0


def test_d_core_tension_always_exists_for_complete_case(son_output) -> None:
    """D. Core tension always exists for a complete case."""
    thesis = generate_case_thesis(build_composer_input_from_production(son_output))
    assert thesis.status == "complete"
    assert thesis.core_tension
    assert thesis.core_tension_present == 1.0


def test_e_corrective_direction_always_exists_for_complete_case(son_output) -> None:
    """E. Corrective direction always exists for a complete case."""
    thesis = generate_case_thesis(build_composer_input_from_production(son_output))
    assert thesis.corrective_direction
    assert thesis.corrective_direction_present == 1.0


def test_f_shensha_cannot_become_primary_thesis_owner() -> None:
    """F. Shen Sha cannot become the primary thesis owner."""
    focus = ChartFocus(
        selected="Thực Thần",
        favorable=("Thực Thần",),
        unfavorable=("Tỷ Kiên",),
        pattern_label="Chính Ấn",
        strength_label="Thân vượng",
        strength_state="strong",
        canonical_shensha=("Hồng Loan", "Hoa Cái"),
    )
    thesis = generate_case_thesis(_input_from_focus(focus))
    blob = f"{thesis.title} {thesis.short_thesis} {thesis.thesis_key}"
    assert "Hồng Loan" not in thesis.title
    assert "Hoa Cái" not in thesis.title
    assert thesis.tension_id != "hong_loan"
    assert "Hồng Loan" not in thesis.thesis_key
    assert "support" in thesis.pattern_function
    assert "Hồng Loan" not in blob.split("Người")[0] or thesis.useful_function != "shensha"


def test_g_son_thesis_generated_without_hardcoding(son_output) -> None:
    """G. Sơn thesis generated without hardcoding."""
    source = build_composer_input_from_production(son_output)
    thesis = generate_case_thesis(source)
    assert source.chart_focus is not None
    assert source.chart_focus.selected == "Chính Quan"
    assert thesis.strength_function == "surplus"
    assert thesis.pattern_function == "support"
    assert thesis.ky_function == "peer"
    assert thesis.tension_id == "responsibility_vs_competition"
    assert thesis.short_thesis
    assert "chắc chắn" not in thesis.short_thesis
    assert "sinh ra để" not in thesis.short_thesis


def test_h_tan_thesis_generated_without_hardcoding() -> None:
    """H. Tân thesis generated without hardcoding."""
    thesis = generate_case_thesis(_input_from_focus(_tan_focus()))
    assert thesis.status == "complete"
    assert thesis.strength_function == "balance"
    assert thesis.pattern_function == "support"
    assert thesis.useful_function in {"discipline", "resource"}
    assert thesis.ky_function in {"growth", "support"}
    assert thesis.tension_id == "growth_vs_containment"
    assert "Mộc" in thesis.supporting_facts or "trung hòa" in thesis.short_thesis.casefold()
    assert "Hồng Loan" not in thesis.title


def test_i_son_and_tan_are_materially_different(son_output) -> None:
    """I. Sơn and Tân are materially different."""
    son = generate_case_thesis(build_composer_input_from_production(son_output))
    tan = generate_case_thesis(_input_from_focus(_tan_focus()))
    comparison = compare_case_theses(son, tan)
    assert son.title != tan.title
    assert son.short_thesis != tan.short_thesis
    assert son.core_tension != tan.core_tension
    assert son.corrective_direction != tan.corrective_direction
    assert son.career_implication != tan.career_implication
    assert son.primary_risks != tan.primary_risks
    assert son.tension_id != tan.tension_id
    assert comparison.structural_similarity < CROSS_CASE_SIMILARITY_MAX
    assert comparison.overgeneralized is False


def test_j_huynh_materially_differs_from_both(son_output, huynh_output) -> None:
    """J. Huỳnh materially differs from both Sơn and Tân."""
    son = generate_case_thesis(build_composer_input_from_production(son_output))
    huynh = generate_case_thesis(build_composer_input_from_production(huynh_output))
    tan = generate_case_thesis(_input_from_focus(_tan_focus()))
    assert huynh.status == "complete"
    assert huynh.core_pattern != son.core_pattern or huynh.useful_function != son.useful_function
    assert huynh.title != son.title
    assert huynh.title != tan.title
    assert huynh.core_pattern != son.core_pattern or huynh.useful_function != son.useful_function
    assert compare_case_theses(huynh, son).structural_similarity < CROSS_CASE_SIMILARITY_MAX
    assert compare_case_theses(huynh, tan).structural_similarity < CROSS_CASE_SIMILARITY_MAX


def test_k_same_analytical_structure_may_produce_similar_thesis() -> None:
    """K. Same analytical structure may legitimately produce similar thesis."""
    focus = ChartFocus(
        selected="Thực Thần",
        favorable=("Thực Thần", "Thương Quan"),
        unfavorable=("Tỷ Kiên", "Kiếp Tài"),
        pattern_label="Chính Ấn",
        strength_label="Thân vượng",
        strength_state="strong",
    )
    twin = replace(focus, current_dayun="Ất Tỵ 2022–2031")
    left = generate_case_thesis(_input_from_focus(focus))
    right = generate_case_thesis(_input_from_focus(twin))
    comparison = compare_case_theses(left, right)
    assert left.title == right.title
    assert left.tension_id == right.tension_id
    assert comparison.overgeneralized is False
    assert comparison.structural_similarity >= CROSS_CASE_SIMILARITY_MAX


def test_l_different_structures_trigger_overgeneralization_if_collapsed() -> None:
    """L. Different analytical structures trigger overgeneralization if thesis collapses."""
    son_like = generate_case_thesis(
        _input_from_focus(
            ChartFocus(
                selected="Thực Thần",
                favorable=("Thực Thần",),
                unfavorable=("Tỷ Kiên",),
                pattern_label="Chính Ấn",
                strength_label="Thân vượng",
                strength_state="strong",
            )
        )
    )
    tan_like = generate_case_thesis(_input_from_focus(_tan_focus()))
    collapsed = replace(
        tan_like,
        title=son_like.title,
        short_thesis=son_like.short_thesis,
        tension_id=son_like.tension_id,
        corrective_id=son_like.corrective_id,
    )
    comparison = compare_case_theses(son_like, collapsed)
    assert comparison.overgeneralized is True
    assert "case_thesis_overgeneralized" in comparison.diagnostics


def test_m_narrative_composer_consumes_thesis(son_output) -> None:
    """M. Narrative Composer consumes thesis."""
    result = compose_narrative_v2_from_production(son_output)
    assert result.case_thesis is not None
    assert result.case_thesis.status == "complete"
    payload = result.to_dict()
    assert payload["case_thesis"]["title"] == result.case_thesis.title


def test_n_executive_summary_begins_from_thesis(son_output) -> None:
    """N. Executive Summary begins from thesis."""
    result = compose_narrative_v2_from_production(son_output)
    summary = result.section("Executive Summary")
    assert summary is not None
    assert summary.sentences
    thesis = result.case_thesis
    assert thesis is not None
    first = summary.sentences[0].text
    assert thesis.title in first or first in thesis.short_thesis or thesis.title == first


def test_o_reasoning_supports_thesis_rather_than_dumping_bundles(son_output) -> None:
    """O. Reasoning supports thesis rather than dumping bundles."""
    result = compose_narrative_v2_from_production(son_output)
    reasoning = result.section("Reasoning")
    assert reasoning is not None
    blob = " ".join(sentence.text for sentence in reasoning.sentences)
    thesis = result.case_thesis
    assert thesis is not None
    assert thesis.core_pattern in blob or thesis.core_strength in blob
    assert "Career:" not in blob


def test_p_recommendation_follows_corrective_direction(son_output) -> None:
    """P. Recommendation follows corrective direction."""
    result = compose_narrative_v2_from_production(son_output)
    recs = result.section("Recommendation")
    assert recs is not None
    assert recs.sentences
    thesis = result.case_thesis
    assert thesis is not None
    blob = " ".join(sentence.text for sentence in recs.sentences).casefold()
    assert any(
        token in blob
        for token in ("hoàn thành", "sản phẩm", "đầu ra", "biểu đạt", "thực", "kênh")
    )


def test_q_conclusion_returns_to_thesis(son_output) -> None:
    """Q. Conclusion returns to thesis."""
    result = compose_narrative_v2_from_production(son_output)
    conclusion = result.section("Conclusion")
    assert conclusion is not None
    blob = " ".join(sentence.text for sentence in conclusion.sentences)
    thesis = result.case_thesis
    assert thesis is not None
    assert thesis.title in blob or thesis.corrective_direction in blob


def test_r_no_ui_dependency() -> None:
    """R. No UI dependency."""
    for path in _NARRATIVE_ROOT.rglob("*.py"):
        if "case_thesis" not in path.as_posix() and path.name not in {
            "composer.py",
            "renderer.py",
            "result_v2.py",
            "__init__.py",
        }:
            continue
        source = path.read_text(encoding="utf-8")
        for marker in _FORBIDDEN_UI_IMPORTS:
            assert marker not in source, path


def test_s_no_engine_changes() -> None:
    """S. No engine changes — thesis does not import analytical engines."""
    root = _NARRATIVE_ROOT / "case_thesis"
    for path in root.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        for marker in _FORBIDDEN_ENGINE_IMPORTS:
            assert marker not in source, f"{path}: {marker}"


def test_t_no_person_name_hardcoding() -> None:
    """T. No person-name hardcoding."""
    root = _NARRATIVE_ROOT / "case_thesis"
    for path in root.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        for name in _PERSON_NAMES:
            assert name not in source, f"{path}: {name}"


def test_composer_uses_tan_thesis_spine() -> None:
    """Tân constructed case still organizes Executive Summary from thesis."""
    result = compose_narrative_v2(_input_from_focus(_tan_focus()), debug_mode=True)
    assert result.case_thesis is not None
    summary = result.section("Executive Summary")
    assert summary is not None
    assert summary.sentences
    assert result.case_thesis.title in summary.sentences[0].text
    conclusion = result.section("Conclusion")
    assert conclusion is not None
    assert result.case_thesis.title in " ".join(item.text for item in conclusion.sentences)
