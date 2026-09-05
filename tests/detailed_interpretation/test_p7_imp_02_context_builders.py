"""P7-IMP-02 context builders: containers only, no reasoning."""

from __future__ import annotations

from engines.detailed_interpretation_engine.builders import (
    CanonicalAnalysisContextBuilder,
    DomainContextBuilder,
    EvidenceContextBuilder,
    InterpretationContextBuilder,
    NarrativeContextBuilder,
    OptimizationContextBuilder,
    TemporalContextBuilder,
    build_canonical_analysis_context_from_payload,
)
from engines.detailed_interpretation_engine.enums import DomainState, EvaluationStatus
from engines.detailed_interpretation_engine.factories import (
    build_canonical_analysis_context,
    build_domain_context,
    build_evidence_context,
    build_interpretation_context,
    build_narrative_context,
    build_optimization_context,
    build_temporal_context,
)
from engines.detailed_interpretation_engine.service import DetailedInterpretationService


SAMPLE_PAYLOAD = {
    "analysis_id": "an-p7-ctx-001",
    "pattern": {"cach_cuc": "Chinh An", "pattern": "Chinh An"},
    "score": {"grade": "B"},
    "strength": {"strength_level": "balanced"},
    "useful_god": {"useful_display": "Thuy", "useful_god": "Thuy"},
    "temperature": {"climate_state": "warm"},
    "five_elements": {"wood": {"count": 2}},
    "identity": {
        "person": {"solar_birth": "1990-05-15", "gender": "male", "timezone": "Asia/Ho_Chi_Minh"},
        "calendar": {"solar_date": "1990-05-15", "lunar_date": "1990-04-21"},
        "four_pillars": {"hour": {"stem": "Ky", "branch": "Ti"}},
    },
}


def test_builder_classes_exist() -> None:
    assert InterpretationContextBuilder
    assert EvidenceContextBuilder
    assert DomainContextBuilder
    assert TemporalContextBuilder
    assert OptimizationContextBuilder
    assert NarrativeContextBuilder
    assert CanonicalAnalysisContextBuilder


def test_interpretation_context_collects_upstream_refs_only() -> None:
    context = InterpretationContextBuilder().build_from_payload(SAMPLE_PAYLOAD)
    assert context.analysis_id == "an-p7-ctx-001"
    assert context.pattern_ref == "Chinh An"
    assert context.grade_ref == "B"
    assert context.strength_ref == "balanced"
    assert context.useful_god_ref == "Thuy"
    assert context.temperature_ref == "warm"
    assert context.five_elements_ref == "five_elements"
    assert context.integrity_ref == ""
    assert context.mc01.status is EvaluationStatus.NOT_EVALUATED
    assert context.chart_identity.birth_civil == "1990-05-15"


def test_evidence_context_is_empty_container() -> None:
    context = build_evidence_context("an-p7-ctx-001")
    assert context.analysis_id == "an-p7-ctx-001"
    assert context.status is EvaluationStatus.NOT_EVALUATED
    assert context.evidence.ranked_domains == ()
    assert context.evidence.dominant_evidence == ()
    assert context.evidence.status is EvaluationStatus.NOT_EVALUATED


def test_domain_context_has_six_structural_containers() -> None:
    context = build_domain_context("an-p7-ctx-001")
    assert context.authority.natal.domain_id == "authority"
    assert context.career.natal.domain_id == "career"
    assert context.wealth.natal.domain_id == "wealth"
    assert context.relationship.natal.domain_id == "relationship"
    assert context.legacy.natal.domain_id == "legacy"
    assert context.vitality.natal.domain_id == "vitality"
    assert context.authority.natal.state is DomainState.NOT_EVALUATED
    assert context.status is EvaluationStatus.NOT_EVALUATED


def test_temporal_optimization_narrative_are_not_evaluated() -> None:
    temporal = build_temporal_context("an-p7-ctx-001")
    optimization = build_optimization_context("an-p7-ctx-001")
    narrative = build_narrative_context("an-p7-ctx-001")
    assert temporal.luck.status is EvaluationStatus.NOT_EVALUATED
    assert temporal.interaction.status is EvaluationStatus.NOT_EVALUATED
    assert temporal.temporal.state is EvaluationStatus.NOT_EVALUATED
    assert optimization.inputs.state is EvaluationStatus.NOT_EVALUATED
    assert optimization.inputs.actions == ()
    assert narrative.inputs.graph.nodes == ()
    assert narrative.inputs.result.status is EvaluationStatus.NOT_EVALUATED


def test_canonical_chain_shares_analysis_id_and_stays_not_evaluated() -> None:
    chain = build_canonical_analysis_context(payload=SAMPLE_PAYLOAD)
    analysis_id = "an-p7-ctx-001"
    assert chain.analysis_id == analysis_id
    assert chain.interpretation.analysis_id == analysis_id
    assert chain.evidence.analysis_id == analysis_id
    assert chain.domain.analysis_id == analysis_id
    assert chain.temporal.analysis_id == analysis_id
    assert chain.optimization.analysis_id == analysis_id
    assert chain.narrative.analysis_id == analysis_id
    assert chain.runtime.analysis_id == analysis_id
    assert chain.status is EvaluationStatus.NOT_EVALUATED
    assert chain.runtime.interpretation.status is EvaluationStatus.NOT_EVALUATED
    assert chain.runtime.context_ref == chain.context_ref
    assert chain.context_ref.startswith("ctx-")


def test_service_build_contexts_matches_factory() -> None:
    service = DetailedInterpretationService()
    chain = service.build_contexts(SAMPLE_PAYLOAD)
    assert chain.interpretation.pattern_ref == "Chinh An"
    assert chain.evidence.evidence.ranked_domains == ()


def test_analyze_payload_does_not_expose_pack07_context() -> None:
    from applications.api.services.orchestrator import (
        OrchestratorService,
        _INTERNAL_PAYLOAD_KEYS,
    )

    assert "pack07_context" in _INTERNAL_PAYLOAD_KEYS
    assert "_pack07_context" in _INTERNAL_PAYLOAD_KEYS
    orch = OrchestratorService()
    analysis = _dummy_analysis()
    payload = {
        "analysis_id": "an-p7-ctx-001",
        "pattern": {"cach_cuc": "Chinh An"},
        "score": {"grade": "B"},
        "calendar": {"solar_date": "1990-05-15"},
    }
    orch._attach_pack07_context(analysis, payload)
    assert analysis.pack07_context is not None
    assert analysis.pack07_context.status is EvaluationStatus.NOT_EVALUATED
    assert analysis.pack07_context.interpretation.pattern_ref == "Chinh An"


def _dummy_analysis():
    from applications.api.models.analysis_result import AnalysisResult, BaziView, PillarView

    pillar = PillarView(stem="Giap", branch="Dan")
    return AnalysisResult(
        bazi=BaziView(
            year_pillar=pillar,
            month_pillar=pillar,
            day_pillar=pillar,
            hour_pillar=pillar,
            day_master="Giap",
            day_master_element="wood",
            day_master_yin_yang="yang",
        )
    )


def test_build_interpretation_context_factory_backward_compatible() -> None:
    context = build_interpretation_context("an-p7-legacy")
    assert context.analysis_id == "an-p7-legacy"
    assert context.pattern_ref == ""
    assert context.mc01.status is EvaluationStatus.NOT_EVALUATED


def test_canonical_builder_from_payload_helper() -> None:
    chain = build_canonical_analysis_context_from_payload(SAMPLE_PAYLOAD)
    assert CanonicalAnalysisContextBuilder().build_from_payload(SAMPLE_PAYLOAD).analysis_id == (
        chain.analysis_id
    )
    assert chain.interpretation.five_elements_ref == "five_elements"
