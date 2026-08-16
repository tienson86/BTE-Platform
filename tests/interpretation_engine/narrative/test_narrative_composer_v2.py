"""Sprint N1 — Narrative Composer V2 tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.models import ProductionRequest
from engines.interpretation_engine.foundation.narrative import (
    CUSTOMER_DOMAINS,
    NARRATIVE_SECTIONS,
    NarrativeComposerInput,
    NarrativeComposerV2,
    compose_narrative_v2,
    compose_narrative_v2_from_production,
)
from engines.interpretation_engine.foundation.narrative.constants import (
    KIND_APPLICATION,
    KIND_CONCLUSION,
    KIND_EVIDENCE,
    KIND_FACT,
    KIND_REASON,
    KIND_RECOMMENDATION,
    KIND_WARNING,
    SLOT_CONCLUSION,
    SLOT_IMPACT,
    SLOT_OBSERVATION,
    SLOT_REASONING,
    SLOT_RECOMMENDATION,
    SLOT_SUMMARY,
    SLOT_WARNING,
)
from engines.interpretation_engine.foundation.narrative.input import (
    CopiedStatement,
    DecisionBundle,
    KnowledgeBundle,
    RelationshipBundle,
    StateBundle,
)
from engines.interpretation_engine.foundation.narrative.text import fingerprint

HUYNH = ProductionRequest(
    year=1966,
    month=9,
    day=24,
    hour=4,
    minute=15,
    gender="male",
    full_name="Lương Ngọc Huỳnh",
)

_NARRATIVE_DIR = Path("engines/interpretation_engine/foundation/narrative")


def test_architecture_accepts_only_four_bundle_kinds() -> None:
    """Composer input is Decision, State, Relationship, Knowledge only."""
    source = _synthetic_input()
    payload = source.to_dict()
    assert payload["accepted_kinds"] == [
        "decision",
        "state",
        "relationship",
        "knowledge",
    ]
    assert set(payload) <= {
        "accepted_kinds",
        "decision_bundles",
        "state_bundles",
        "relationship_bundles",
        "knowledge_bundles",
    }


def test_pipeline_produces_seven_sections() -> None:
    """Frozen pipeline renders every canonical section."""
    result = NarrativeComposerV2().compose(_synthetic_input())
    assert tuple(section.name for section in result.sections) == NARRATIVE_SECTIONS
    for section in result.sections:
        assert section.sentences, section.name
        assert section.evidence_ids


def test_evidence_composer_does_not_infer_missing_facts() -> None:
    """Missing statements stay missing. No new facts are generated."""
    source = NarrativeComposerInput(
        decision_bundles=(
            DecisionBundle(
                bundle_id="decision:UsefulGod",
                domain="UsefulGod",
                selected="Đinh",
                reason="selected by engine",
                confidence=0.9,
                importance=1.0,
                statements=(
                    CopiedStatement(
                        text="Đinh",
                        kind=KIND_CONCLUSION,
                        slot=SLOT_SUMMARY,
                        engine_truth_ref="decision:selected",
                        confidence=0.9,
                    ),
                ),
                engine_truth_refs=("rule_ug_01",),
            ),
        )
    )
    result = compose_narrative_v2(source)
    statements = [node.statement for node in result.evidence.nodes]
    assert "Đinh" in statements
    assert all("inferred" not in item.casefold() for item in statements)
    assert all("missing" not in item.casefold() for item in statements)


def test_reason_composer_builds_structured_chains() -> None:
    """Reason Composer emits Fact → Evidence → Reason → Conclusion, not prose pages."""
    result = compose_narrative_v2(_synthetic_input())
    assert result.reasoning_chains
    chain = result.reasoning_chains[0]
    assert chain.fact
    assert chain.reason
    assert chain.conclusion
    assert chain.fact_ids
    assert chain.evidence_ids
    assert chain.reason_id
    assert chain.conclusion_id


def test_application_composer_maps_supported_customer_domains() -> None:
    """Applications map to the seven customer domains and do not predict outcomes."""
    result = compose_narrative_v2(_synthetic_input())
    domains = {item.customer_domain for item in result.applications}
    assert domains <= set(CUSTOMER_DOMAINS)
    assert "Career" in domains
    assert "Finance" in domains
    joined = " ".join(item.statement for item in result.applications).casefold()
    assert "will become" not in joined
    assert "chắc chắn" not in joined


def test_recommendations_never_come_from_score() -> None:
    """Score-shaped engine refs are rejected. Recs keep evidence ids."""
    source = _synthetic_input()
    scored = CopiedStatement(
        text="Raise the score to succeed",
        kind=KIND_RECOMMENDATION,
        slot=SLOT_RECOMMENDATION,
        engine_truth_ref="state:Strength:score",
        confidence=0.5,
    )
    state = source.state_bundles[0]
    poisoned = StateBundle(
        bundle_id=state.bundle_id,
        domain=state.domain,
        state=state.state,
        label=state.label,
        confidence=state.confidence,
        importance=state.importance,
        statements=(*state.statements, scored),
        engine_truth_refs=state.engine_truth_refs,
    )
    result = compose_narrative_v2(
        NarrativeComposerInput(
            decision_bundles=source.decision_bundles,
            state_bundles=(poisoned,),
            relationship_bundles=source.relationship_bundles,
            knowledge_bundles=source.knowledge_bundles,
        )
    )
    actions = [item.action for item in result.recommendations]
    assert "Raise the score to succeed" not in actions
    assert result.recommendations
    for item in result.recommendations:
        assert item.evidence_ids


def test_deduplication_merges_repeated_ideas() -> None:
    """Duplicate evidence, recommendations, and warnings collapse before render."""
    result = compose_narrative_v2(_synthetic_input())
    assert result.evidence.raw_count > result.evidence.merged_count
    rec_marks = [fingerprint(item.action) for item in result.recommendations]
    warn_marks = [fingerprint(item.risk) for item in result.warnings]
    assert len(rec_marks) == len(set(rec_marks))
    assert len(warn_marks) == len(set(warn_marks))
    reasoning = result.section("Reasoning")
    assert reasoning is not None
    reason_marks = [fingerprint(sentence.text) for sentence in reasoning.sentences]
    assert len(reason_marks) == len(set(reason_marks))


def test_prioritization_keeps_higher_ranked_bundle() -> None:
    """Same customer topic keeps the higher domain-priority implication."""
    result = compose_narrative_v2(_synthetic_input())
    career = [item for item in result.applications if item.customer_domain == "Career"]
    assert career
    assert career[0].domain == "UsefulGod"


def test_every_sentence_is_traceable() -> None:
    """Sentence → evidence → bundle → engine truth. No orphans."""
    result = compose_narrative_v2(_synthetic_input())
    assert result.metrics.orphan_sentence_count == 0
    assert result.metrics.traceability_coverage == 1.0
    assert len(result.traceability) == result.metrics.sentence_count
    for record in result.traceability:
        assert record.evidence_ids
        assert record.bundle_ids
        assert record.engine_truth_refs
        node = result.evidence.get(record.evidence_ids[0])
        assert node is not None
        assert node.bundle_id in record.bundle_ids


def test_metrics_are_present() -> None:
    """Composer metrics cover evidence, duplicates, reasons, recs, warnings, trace."""
    metrics = compose_narrative_v2(_synthetic_input()).metrics
    payload = metrics.to_dict()
    for key in (
        "evidence_coverage",
        "duplicate_ratio",
        "reason_coverage",
        "recommendation_coverage",
        "warning_coverage",
        "traceability_coverage",
    ):
        assert key in payload
        assert 0.0 <= payload[key] <= 1.0
    assert metrics.duplicate_ratio > 0.0
    assert metrics.sentence_count > 0


def test_v2_does_not_import_pack05_narrative_engine() -> None:
    """V2 coexists with Pack 05. It must not call or import NarrativeEngine."""
    for path in _NARRATIVE_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "from engines.narrative_engine" not in source
        assert "import NarrativeEngine" not in source


def test_golden_huynh_composes_all_bundles_without_missing_sections(
    huynh_output,
) -> None:
    """Lương Ngọc Huỳnh: UsefulGod + Pattern + Strength + TenGods + ShenSha."""
    source = _input_from_production(huynh_output)
    domains = {bundle.domain for bundle in source.all_bundles()}
    assert domains >= {"UsefulGod", "Strength", "Pattern", "TenGods", "ShenSha"}
    assert source.decision_bundles
    assert source.state_bundles
    assert {item.domain for item in source.relationship_bundles} >= {
        "Pattern",
        "TenGods",
        "ShenSha",
    }
    result = compose_narrative_v2_from_production(huynh_output)
    assert result.diagnostics == ()
    for name in NARRATIVE_SECTIONS:
        section = result.section(name)
        assert section is not None
        assert section.sentences, name
    reasoning = result.section("Reasoning")
    assert reasoning is not None
    marks = [fingerprint(sentence.text) for sentence in reasoning.sentences]
    assert len(marks) == len(set(marks))
    assert result.metrics.traceability_coverage == 1.0
    assert result.metrics.orphan_sentence_count == 0
    assert result.reasoning_chains
    assert result.recommendations
    assert result.warnings
    blob = result.to_dict()
    assert "Lương Ngọc Huỳnh" not in str(blob)


def test_reasoning_is_grouped_by_customer_topic() -> None:
    """Reasoning is a consultation chain, not an engine or English-tagged dump."""
    result = compose_narrative_v2(_synthetic_input())
    reasoning = result.section("Reasoning")
    assert reasoning is not None
    engines = {"UsefulGod", "Strength", "Pattern", "TenGods", "ShenSha"}
    english_tags = {"Career", "Health", "Decision", "Finance", "Environment", "Learning"}
    for sentence in reasoning.sentences:
        prefix = sentence.text.split(":", 1)[0].strip()
        assert prefix not in engines
        assert prefix not in english_tags
    assert reasoning.sentences


def test_renderer_has_no_fixed_sentence_budget() -> None:
    """Coverage ranking replaced the old 8-sentence cap."""
    source = (_NARRATIVE_DIR / "renderer.py").read_text(encoding="utf-8")
    assert "_SECTION_CAP" not in source


def test_golden_huynh_explains_decision_state_and_relationships(
    huynh_output,
) -> None:
    """Huỳnh live narrative must explain Đinh, rejected Bính, Chính Tài, thân vượng, Hỷ/Kỵ."""
    result = compose_narrative_v2_from_production(huynh_output)
    blob = " ".join(
        sentence.text
        for section in result.sections
        for sentence in section.sentences
    )
    assert "Đinh" in blob
    assert "Bính" in blob
    assert "Chính Tài" in blob
    assert "vượng" in blob or "strong" in blob.casefold()
    assert "Hỷ" in blob
    assert "Kỵ" in blob
    assert any(role in blob for role in ("Nhật Chủ", "Kiếp Tài", "Thiên Tài"))
    assert "day_master=" not in blob
    assert "group priority" not in blob.casefold()
    reasoning = result.section("Reasoning")
    assert reasoning is not None
    recs = [sentence.text for sentence in result.section("Recommendation").sentences]
    assert recs
    assert len(recs) == len({fingerprint(item) for item in recs})
    assert recs[0].startswith("1.")
    assert "Career:" not in " ".join(recs)
    assert "Decision:" not in " ".join(recs)


def test_narrative_result_v2_keeps_live_report_section_ids(huynh_output) -> None:
    """Adapter emits the live Portal/PDF section ids without a UI redesign."""
    from engines.interpretation_engine.foundation.narrative import (
        narrative_result_v2_to_dict,
    )
    from engines.report_engine.narrative_binding import CANONICAL_SECTION_IDS

    result = compose_narrative_v2_from_production(huynh_output)
    payload = narrative_result_v2_to_dict(result, run_id="huynh")
    assert payload["generator"] == "narrative_composer_v2"
    assert payload["contract"] == "pack05_narrative_result_v1"
    assert [section["id"] for section in payload["sections"]] == list(CANONICAL_SECTION_IDS)
    for section in payload["sections"]:
        assert section["paragraphs"]
        for paragraph in section["paragraphs"]:
            assert paragraph["evidence_refs"]


def test_pack05_narrative_engine_still_importable() -> None:
    """Old renderer remains available during migration."""
    from engines.narrative_engine.engine import NarrativeEngine

    assert NarrativeEngine is not None


@pytest.fixture(scope="module")
def huynh_output():
    """Production pipeline output for Lương Ngọc Huỳnh."""
    return ProductionEngineRunner().run(HUYNH)


def _input_from_production(output) -> NarrativeComposerInput:
    """Build frozen composer input from production without recalculating."""
    from engines.interpretation_engine.foundation.narrative.production import (
        build_composer_input_from_production,
    )

    return build_composer_input_from_production(output)


def _synthetic_input() -> NarrativeComposerInput:
    """Minimal already-validated bundles covering every composer stage."""
    shared_career = "Hợp việc có trách nhiệm nguồn, không suy ra một nghề."
    shared_rec = "Mở một kênh thoát có phép."
    shared_warn = "Sức dư không dẫn sẽ dồn áp."
    decision = DecisionBundle(
        bundle_id="decision:UsefulGod",
        domain="UsefulGod",
        selected="Đinh",
        reason="Engine selected Đinh",
        confidence=0.9,
        importance=1.0,
        statements=(
            CopiedStatement(
                text="Đinh",
                kind=KIND_CONCLUSION,
                slot=SLOT_SUMMARY,
                engine_truth_ref="useful_god.selected",
                confidence=0.9,
            ),
            CopiedStatement(
                text="Engine selected Đinh",
                kind=KIND_REASON,
                slot=SLOT_SUMMARY,
                engine_truth_ref="useful_god.reason",
                confidence=0.9,
            ),
            CopiedStatement(
                text="day_master=Bính",
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="bazi.day_master",
                confidence=0.9,
            ),
            CopiedStatement(
                text="Nhật chủ Bính copied again",
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="bazi.day_master",
                confidence=0.8,
            ),
            CopiedStatement(
                text="rule=ug_dinh",
                kind=KIND_EVIDENCE,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="rule_ug_dinh",
                confidence=0.9,
            ),
            CopiedStatement(
                text="Season and flow favor Đinh",
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref="useful_god.path.season",
                confidence=0.9,
            ),
            CopiedStatement(
                text="Dụng thần là Đinh",
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref="useful_god.meaning",
                confidence=0.9,
            ),
            CopiedStatement(
                text=shared_career,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref="useful_god.applications.career",
                customer_domain="Career",
                confidence=0.9,
            ),
            CopiedStatement(
                text="Thiên tích có kế hoạch, không hứa hiệu quả tài chính.",
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref="useful_god.applications.wealth",
                customer_domain="Finance",
                confidence=0.9,
            ),
            CopiedStatement(
                text=shared_rec,
                kind=KIND_RECOMMENDATION,
                slot=SLOT_RECOMMENDATION,
                engine_truth_ref="useful_god.advice.flow",
                rationale="Dẫn sức dư thành việc.",
                category="energy_management",
                confidence=0.9,
            ),
            CopiedStatement(
                text=shared_warn,
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref="useful_god.warning.over",
                condition="over_accumulation",
                mitigation="Giữ một kênh thoát.",
                confidence=0.9,
            ),
        ),
        engine_truth_refs=("useful_god.selected", "rule_ug_dinh"),
    )
    state = StateBundle(
        bundle_id="state:Strength",
        domain="Strength",
        state="strong",
        label="Thân vượng",
        confidence=0.8,
        importance=0.85,
        statements=(
            CopiedStatement(
                text="strong",
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="strength.level",
                confidence=0.8,
            ),
            CopiedStatement(
                text="strong",
                kind=KIND_CONCLUSION,
                slot=SLOT_SUMMARY,
                engine_truth_ref="strength.level",
                confidence=0.8,
            ),
            CopiedStatement(
                text="Thân vượng",
                kind=KIND_FACT,
                slot=SLOT_SUMMARY,
                engine_truth_ref="strength.label",
                confidence=0.8,
            ),
            CopiedStatement(
                text="Season=strong",
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref="strength.path.season",
                confidence=0.8,
            ),
            CopiedStatement(
                text="support=0.7",
                kind=KIND_EVIDENCE,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="strength.evidence.support",
                confidence=0.8,
            ),
            CopiedStatement(
                text=shared_rec,
                kind=KIND_RECOMMENDATION,
                slot=SLOT_RECOMMENDATION,
                engine_truth_ref="strength.recommendation.flow",
                confidence=0.8,
            ),
            CopiedStatement(
                text=shared_warn,
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref="strength.warning.over",
                confidence=0.8,
            ),
        ),
        engine_truth_refs=("pri_level_strong",),
    )
    relationship = RelationshipBundle(
        bundle_id="relationship:Pattern",
        domain="Pattern",
        confidence=0.7,
        importance=0.7,
        statements=(
            CopiedStatement(
                text="Chính Tài",
                kind=KIND_FACT,
                slot=SLOT_SUMMARY,
                engine_truth_ref="pattern.selected",
                confidence=0.7,
            ),
            CopiedStatement(
                text="month_command:Chính Tài",
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="pattern.month_command",
                confidence=0.7,
            ),
            CopiedStatement(
                text="month_command->generates->pattern:chinh_tai",
                kind=KIND_REASON,
                slot=SLOT_REASONING,
                engine_truth_ref="pattern.edge.generates",
                confidence=0.7,
            ),
            CopiedStatement(
                text="Cục lấy việc đổi sức thành nguồn có sổ làm trục.",
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref="pattern.meaning",
                confidence=0.7,
            ),
            CopiedStatement(
                text=shared_career,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref="pattern.applications.career",
                customer_domain="Career",
                confidence=0.7,
            ),
            CopiedStatement(
                text="Giữ sổ; cắt nghĩa vụ vượt lệnh.",
                kind=KIND_RECOMMENDATION,
                slot=SLOT_RECOMMENDATION,
                engine_truth_ref="pattern.recommendation.boundary",
                confidence=0.7,
            ),
            CopiedStatement(
                text="Nghĩa vụ nguồn quá nền làm kiệt nhật chủ.",
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref="pattern.warning.over_obligation",
                mitigation="Giữ sổ.",
                confidence=0.7,
            ),
        ),
        engine_truth_refs=("pat_ct_01",),
    )
    knowledge = KnowledgeBundle(
        bundle_id="knowledge:UsefulGod",
        domain="UsefulGod",
        entity_keys=("Đinh",),
        confidence=0.9,
        importance=0.6,
        statements=(
            CopiedStatement(
                text="Đinh — kênh dẫn",
                kind=KIND_FACT,
                slot=SLOT_OBSERVATION,
                engine_truth_ref="knowledge.useful_god.dinh:title",
                confidence=0.9,
            ),
            CopiedStatement(
                text="Dụng thần là Đinh",
                kind=KIND_CONCLUSION,
                slot=SLOT_CONCLUSION,
                engine_truth_ref="knowledge.useful_god.dinh:meaning",
                confidence=0.9,
            ),
            CopiedStatement(
                text=shared_career,
                kind=KIND_APPLICATION,
                slot=SLOT_IMPACT,
                engine_truth_ref="knowledge.useful_god.dinh:career",
                customer_domain="Career",
                confidence=0.9,
            ),
            CopiedStatement(
                text=shared_rec,
                kind=KIND_RECOMMENDATION,
                slot=SLOT_RECOMMENDATION,
                engine_truth_ref="knowledge.useful_god.dinh:recommendation",
                confidence=0.9,
            ),
            CopiedStatement(
                text=shared_warn,
                kind=KIND_WARNING,
                slot=SLOT_WARNING,
                engine_truth_ref="knowledge.useful_god.dinh:warning",
                confidence=0.9,
            ),
        ),
        engine_truth_refs=("knowledge.useful_god.dinh",),
    )
    return NarrativeComposerInput(
        decision_bundles=(decision,),
        state_bundles=(state,),
        relationship_bundles=(relationship,),
        knowledge_bundles=(knowledge,),
    )
