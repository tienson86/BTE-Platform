"""N2 customer narrative product-repair tests."""

from __future__ import annotations

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.narrative import (
    compose_narrative_v2_from_production,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    COMMERCIAL_RECOMMENDATION_LIMIT,
    KIND_CONCLUSION,
    KIND_FACT,
    KIND_REASON,
    SLOT_CONCLUSION,
    SLOT_OBSERVATION,
    SLOT_REASONING,
)
from engines.interpretation_engine.foundation.narrative.input import (
    CopiedStatement,
    DecisionBundle,
    KnowledgeBundle,
    NarrativeComposerInput,
)
from engines.interpretation_engine.foundation.narrative.production import (
    build_composer_input_from_production,
)
from engines.interpretation_engine.foundation.narrative.quality import (
    hypothetical_knowledge_leak_count,
    implementation_language_count,
)
from engines.interpretation_engine.foundation.narrative.input import ChartFocus
from engines.interpretation_engine.foundation.narrative.relevance import (
    apply_customer_relevance,
)
from engines.interpretation_engine.foundation.narrative.text import is_broken_fragment
from engines.interpretation_engine.foundation.narrative.translation.loader import (
    load_forbidden_terms,
    load_translation_rules,
)

load_translation_rules.cache_clear()
load_forbidden_terms.cache_clear()

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
)


@pytest.fixture(scope="module")
def son_output():
    """Production pipeline output for Nguyễn Tiến Sơn / CASE-0001."""
    return ProductionEngineRunner().run(CASE_0001_REQUEST)


@pytest.fixture(scope="module")
def huynh_output():
    """Production pipeline output for Lương Ngọc Huỳnh."""
    return ProductionEngineRunner().run(HUYNH)


def _blob(result) -> str:
    """Join customer sentences."""
    return " ".join(
        sentence.text
        for section in result.sections
        for sentence in section.sentences
    )


def test_a_relevance_filter_removes_unused_entity_knowledge() -> None:
    """A. Unused entity knowledge is dropped before composition."""
    focus = ChartFocus(selected="Thực Thần", favorable=("Thực Thần",), unfavorable=("Tỷ Kiên",))
    source = NarrativeComposerInput(
        knowledge_bundles=(
            KnowledgeBundle(
                bundle_id="knowledge:UsefulGod",
                domain="UsefulGod",
                entity_keys=("Đinh",),
                confidence=0.9,
                importance=0.6,
                statements=(
                    CopiedStatement(
                        text="Khi Đinh là Dụng thần, giữ lửa vừa.",
                        kind=KIND_CONCLUSION,
                        slot=SLOT_CONCLUSION,
                        engine_truth_ref="knowledge:UsefulGod:Đinh:meaning",
                        confidence=0.9,
                    ),
                ),
                engine_truth_refs=("knowledge.useful_god.dinh",),
            ),
        ),
        chart_focus=focus,
    )
    filtered = apply_customer_relevance(source)
    assert filtered.knowledge_bundles[0].statements == ()


def test_b_selected_hy_ky_knowledge_survives(son_output) -> None:
    """B. Selected / Hỷ / Kỵ knowledge survives for the live Sơn chart."""
    result = compose_narrative_v2_from_production(son_output)
    blob = _blob(result)
    assert "Thực Thần" in blob
    assert "Thương Quan" in blob
    assert "Tỷ Kiên" in blob
    assert "Kiếp Tài" in blob


def test_c_no_hypothetical_role_leakage(son_output) -> None:
    """C. Hypothetical unused-stem roles do not reach the customer."""
    result = compose_narrative_v2_from_production(son_output)
    blob = _blob(result)
    assert "Khi Đinh là Dụng" not in blob
    assert "Khi Quý là Kỵ" not in blob
    assert "Khi Nhâm là Hỷ" not in blob
    assert hypothetical_knowledge_leak_count(result, result_focus(son_output)) == 0


def test_d_useful_god_explanation_remains_complete(son_output) -> None:
    """D. Useful God explanation remains a complete current-chart chain."""
    result = compose_narrative_v2_from_production(son_output)
    reasoning = _blob_section(result, "Reasoning")
    assert "Thực Thần" in reasoning
    assert "vượng" in reasoning or "Thân vượng" in _blob(result)


def test_e_pattern_strength_useful_god_are_synthesized(son_output) -> None:
    """E. Pattern, Strength, and Useful God appear together as one reading."""
    result = compose_narrative_v2_from_production(son_output)
    blob = _blob(result)
    assert "Chính Ấn" in blob
    assert "Thân vượng" in blob or "vượng" in blob
    assert "Thực Thần" in blob
    reasoning = _blob_section(result, "Reasoning")
    assert "Chính Ấn" in reasoning
    assert "Thực Thần" in reasoning


def test_f_recommendation_count_within_commercial_limit(son_output) -> None:
    """F. Customer recommendations stay within the commercial cap."""
    result = compose_narrative_v2_from_production(son_output)
    recs = result.section("Recommendation")
    assert recs is not None
    assert 1 <= len(recs.sentences) <= COMMERCIAL_RECOMMENDATION_LIMIT
    assert result.metrics.recommendation_count <= COMMERCIAL_RECOMMENDATION_LIMIT


def test_g_recommendations_are_priority_ranked(son_output) -> None:
    """G. Recommendations are numbered in priority order."""
    recs = compose_narrative_v2_from_production(son_output).section("Recommendation")
    assert recs is not None
    for index, sentence in enumerate(recs.sentences, start=1):
        assert sentence.text.startswith(f"{index}.")


def test_h_duplicate_recommendation_block_impossible(son_output) -> None:
    """H. The recommendation section cannot reprint the same ranked block."""
    recs = [
        sentence.text
        for sentence in compose_narrative_v2_from_production(son_output)
        .section("Recommendation")
        .sentences
    ]
    assert recs
    assert len(recs) == len(set(recs))


def test_i_implementation_language_gate_remains_clean(son_output) -> None:
    """I. Implementation language does not survive in customer sentences."""
    result = compose_narrative_v2_from_production(son_output)
    blob = _blob(result).casefold()
    for term in (
        "career:",
        "decision explanation",
        "strength engine",
        "production phải",
        "cả hai key",
        "group priority",
        "overusing",
        "ignoring useful god",
    ):
        assert term not in blob
    assert implementation_language_count(result) == 0


def test_j_broken_fragments_fail_validation() -> None:
    """J. Broken fragments are detected and cannot remain in customer input."""
    assert is_broken_fragment("Thực Thần ()")
    assert is_broken_fragment("Tách vs .")
    source = NarrativeComposerInput(
        decision_bundles=(
            DecisionBundle(
                bundle_id="decision:UsefulGod",
                domain="UsefulGod",
                selected="Đinh",
                reason="selected",
                confidence=0.9,
                importance=1.0,
                statements=(
                    CopiedStatement(
                        text="Tách vs .",
                        kind=KIND_REASON,
                        slot=SLOT_REASONING,
                        engine_truth_ref="decision:broken",
                        confidence=0.9,
                    ),
                    CopiedStatement(
                        text="Nhật chủ Bính đủ dài để giữ chuỗi",
                        kind=KIND_FACT,
                        slot=SLOT_OBSERVATION,
                        engine_truth_ref="decision:fact",
                        confidence=0.9,
                    ),
                ),
                engine_truth_refs=("decision:broken",),
            ),
        )
    )
    filtered = apply_customer_relevance(source)
    texts = [item.text for item in filtered.decision_bundles[0].statements]
    assert texts
    assert all("Tách vs" not in item for item in texts)


def test_k_conclusion_does_not_contain_knowledge_catalogue(son_output) -> None:
    """K. Conclusion is a synthesis, not a Ten Gods / stem catalogue."""
    conclusion = _blob_section(
        compose_narrative_v2_from_production(son_output),
        "Conclusion",
    )
    assert "Chính Ấn" in conclusion or "Thực Thần" in conclusion
    assert "Khi Đinh là Dụng" not in conclusion
    assert conclusion.count("Không suy ra") < 8


def test_l_nguyen_tien_son_live_product_acceptance(son_output) -> None:
    """L. Live Nguyễn Tiến Sơn product acceptance."""
    result = compose_narrative_v2_from_production(son_output)
    blob = _blob(result)
    assert result.diagnostics == ()
    assert "Career:" not in blob
    assert "Health:" not in blob
    assert "Decision:" not in blob
    assert "()" not in blob
    assert "Thực Thần" in blob
    assert "Chính Ấn" in blob
    assert "Tỷ Kiên" in blob
    recs = result.section("Recommendation").sentences
    assert 3 <= len(recs) <= 5
    impact = _blob_section(result, "Impact")
    assert "Sự nghiệp" in impact
    assert "Tài chính" in impact
    assert "Quan hệ" in impact
    assert "Sức khỏe" in impact
    assert result.metrics.traceability_coverage == 1.0
    assert result.metrics.broken_fragment_count == 0
    assert result.metrics.hypothetical_knowledge_leak_count == 0


def test_m_luong_ngoc_huynh_regression(huynh_output) -> None:
    """M. Huỳnh keeps Đinh / Chính Tài / Hỷ Đinh-Bính-Ất / Kỵ Canh-Tân."""
    result = compose_narrative_v2_from_production(huynh_output)
    blob = _blob(result)
    assert "Đinh" in blob
    assert "Chính Tài" in blob
    assert "vượng" in blob or "Thân vượng" in blob
    assert "Bính" in blob
    assert "Canh" in blob or "Tân" in blob
    assert "Thực Thần" not in blob or "Đinh" in blob
    assert "Career:" not in blob
    assert result.metrics.traceability_coverage == 1.0


def test_n_traceability_remains_complete(son_output, huynh_output) -> None:
    """N. Rendered claims stay fully traceable."""
    for output in (son_output, huynh_output):
        result = compose_narrative_v2_from_production(output)
        assert result.metrics.traceability_coverage == 1.0
        assert result.metrics.orphan_sentence_count == 0
        for record in result.traceability:
            assert record.evidence_ids
            assert record.bundle_ids
            assert record.engine_truth_refs


def test_o_analytical_truth_unchanged(son_output) -> None:
    """O. Composition does not change Useful God, Strength, or Pattern truth."""
    foundation = son_output.interpretation_foundation
    source = build_composer_input_from_production(son_output)
    selected = source.decision_bundles[0].selected
    assert selected == foundation.useful_god_explanation.decision.selected
    assert selected == "Thực Thần"
    assert source.state_bundles[0].label in {"Thân vượng", "vượng"}
    assert source.chart_focus is not None
    assert source.chart_focus.selected == "Thực Thần"
    assert "Tỷ Kiên" in source.chart_focus.unfavorable
    assert "Kiếp Tài" in source.chart_focus.unfavorable


def test_translation_caches_reload_new_rules() -> None:
    """New translation and forbidden-term files remain loadable."""
    load_translation_rules.cache_clear()
    load_forbidden_terms.cache_clear()
    rules = load_translation_rules()
    assert any(rule.id == "ET-ENG-013" for rule in rules)
    terms = load_forbidden_terms()
    assert "decision explanation" in terms.phrases


def result_focus(output) -> ChartFocus:
    """Read chart focus copied from production without recalculating."""
    focus = build_composer_input_from_production(output).chart_focus
    assert focus is not None
    return focus


def _blob_section(result, name: str) -> str:
    """Join one section's customer sentences."""
    section = result.section(name)
    assert section is not None
    return " ".join(sentence.text for sentence in section.sentences)
