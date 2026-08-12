"""Cross-Domain Reasoning Engine V1.1 tests."""

from __future__ import annotations

import json

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.fixtures.case_0002_readiness import (
    CASE_0002_REQUEST,
    SYNTHETIC_REQUEST_B,
)
from applications.production.interpretation.cross_domain.claim_normalizer import (
    normalize_claims,
)
from applications.production.interpretation.cross_domain.models import (
    ClaimScope,
    CrossDomainReasoningInput,
    QuestionContext,
    RelationType,
    ThemeStatus,
)
from applications.production.interpretation.cross_domain.reasoner import (
    CrossDomainReasoner,
)
from applications.production.interpretation.cross_domain.relation_engine import (
    detect_relations,
    scopes_overlap,
)
from applications.production.interpretation.cross_domain import theme_engine as te
from applications.production.interpretation.service import MultiDomainInterpretationService
from applications.production.orchestrator import ProductionEndToEndOrchestrator


@pytest.fixture(scope="module")
def engine_0001():
    return ProductionEngineRunner().run(CASE_0001_REQUEST)


@pytest.fixture(scope="module")
def engine_0002():
    return ProductionEngineRunner().run(CASE_0002_REQUEST)


@pytest.fixture(scope="module")
def engine_synth():
    return ProductionEngineRunner().run(SYNTHETIC_REQUEST_B)


@pytest.fixture(scope="module")
def composition_0001(engine_0001):
    return MultiDomainInterpretationService().compose(
        case_id="CASE-0001",
        engine_output=engine_0001,
    )


@pytest.fixture(scope="module")
def composition_0002(engine_0002):
    return MultiDomainInterpretationService().compose(
        case_id="CASE-0002",
        engine_output=engine_0002,
    )


@pytest.fixture(scope="module")
def composition_synth(engine_synth):
    return MultiDomainInterpretationService().compose(
        case_id="SYNTHETIC-B",
        engine_output=engine_synth,
    )


def test_claim_normalization() -> None:
    data = CrossDomainReasoningInput(
        strength_level="balanced",
        strength_score=0.61,
        pattern_key="tong_nhi",
        pattern_label="Tòng Nhi — Nhật chủ cực nhược theo Thực/Thương",
        tong_cach="Tòng Nhi",
        ten_gods_primary=["Thương Quan"],
        ten_gods_families=["output"],
        useful_god="Nhâm",
        question_context=QuestionContext.GENERAL,
    )
    claims = normalize_claims(data)
    ids = {c.claim_id for c in claims}
    assert "str_body_level" in ids
    assert "pat_structure" in ids
    assert "pat_follow_flag" in ids
    assert "tg_primary" in ids
    assert "tg_output_family" in ids
    assert "ug_strategy" in ids
    strength = next(c for c in claims if c.claim_id == "str_body_level")
    assert strength.scope == ClaimScope.BODY_STRENGTH


def test_scope_comparison() -> None:
    assert scopes_overlap(ClaimScope.BODY_STRENGTH, ClaimScope.BODY_STRENGTH)
    assert not scopes_overlap(ClaimScope.BODY_STRENGTH, ClaimScope.STRUCTURAL_PATTERN)
    assert scopes_overlap(ClaimScope.GENERAL, ClaimScope.CAREER)


def test_relations_follow_strength_nuance() -> None:
    data = CrossDomainReasoningInput(
        strength_level="balanced",
        strength_score=0.61,
        pattern_key="tong_nhi",
        pattern_label="Tòng Nhi — cực nhược",
        tong_cach="Tòng Nhi",
        ten_gods_primary=["Thương Quan"],
        ten_gods_families=["output"],
        useful_god="Nhâm",
    )
    claims = normalize_claims(data)
    relations = detect_relations(claims)
    types = {r.relation_type for r in relations}
    assert RelationType.DIFFERENT_SCOPE in types
    assert RelationType.DEPENDENCY_OVERRIDE in types
    assert RelationType.CONDITIONAL_NUANCE in types
    assert RelationType.TRUE_CONFLICT not in types


def test_theme_selection_and_suppression() -> None:
    reasoner = CrossDomainReasoner()
    weak_follow = reasoner.reason(
        CrossDomainReasoningInput(
            strength_level="balanced",
            strength_score=0.61,
            pattern_key="tong_nhi",
            pattern_label="Tòng Nhi",
            tong_cach="Tòng Nhi",
            ten_gods_primary=["Thương Quan"],
            ten_gods_families=["output"],
            useful_god="Nhâm",
        )
    )
    theme_ids = {t.theme_id: t for t in weak_follow.themes}
    assert theme_ids[te.THEME_OPERATING_SELF_CARRY].status == ThemeStatus.SUPPRESSED if (
        te.THEME_OPERATING_SELF_CARRY in theme_ids
    ) else True
    assert theme_ids[te.THEME_CAPACITY_STRONG].status == ThemeStatus.SUPPRESSED if (
        te.THEME_CAPACITY_STRONG in theme_ids
    ) else True
    assert te.THEME_OVERLOAD_RISK not in theme_ids or (
        theme_ids[te.THEME_OVERLOAD_RISK].status == ThemeStatus.SUPPRESSED
    )
    assert weak_follow.primary_theme in {
        te.THEME_FOLLOW_STRUCTURE,
        te.THEME_OPERATING_OUTPUT,
        te.THEME_BALANCE_DIRECTION,
        te.THEME_CAPACITY_BALANCED,
    }


def test_question_context_does_not_change_classifications(
    engine_0002,
    composition_0002,
) -> None:
    from applications.production.interpretation.cross_domain.input_builder import (
        build_reasoning_input,
    )

    reasoner = CrossDomainReasoner()
    career = reasoner.reason(
        build_reasoning_input(
            engine_0002,
            composition_0002.domains,
            question_context=QuestionContext.CAREER,
        )
    )
    identity = reasoner.reason(
        build_reasoning_input(
            engine_0002,
            composition_0002.domains,
            question_context=QuestionContext.IDENTITY,
        )
    )
    general = composition_0002.cross_domain
    g_vals = {c.claim_id: c.value for c in general.claims}
    assert g_vals == {c.claim_id: c.value for c in career.claims}
    assert g_vals == {c.claim_id: c.value for c in identity.claims}
    # Salience may differ; facts must not.
    assert career.question_context == QuestionContext.CAREER
    assert identity.question_context == QuestionContext.IDENTITY


def test_executive_claim_plan(composition_0001) -> None:
    plan = composition_0001.cross_domain.executive_claim_plan
    assert plan.identity_core
    assert plan.priorities
    assert plan.avoidances
    assert "." not in plan.primary_insight or len(plan.primary_insight) < 200


def test_anti_overfit_primary_themes(composition_0001, composition_0002) -> None:
    t1 = composition_0001.cross_domain.primary_theme
    t2 = composition_0002.cross_domain.primary_theme
    assert t1 != t2
    body2 = composition_0002.executive.body.lower()
    assert "gánh thêm vô hạn" not in body2
    assert "chuyển tải thành đầu ra có chu kỳ" not in body2
    suppressed = composition_0002.cross_domain.diagnostics.get("suppressed_themes") or []
    assert te.THEME_OPERATING_SELF_CARRY in suppressed or te.THEME_OPERATING_SELF_CARRY not in {
        t.theme_id for t in composition_0002.cross_domain.themes
    }


def test_case_0002_acceptance(composition_0002) -> None:
    cdr = composition_0002.cross_domain
    assert cdr.tensions or cdr.conflicts
    assert "follow_qualifies_strength" in cdr.tensions or any(
        r.relation_type == RelationType.DEPENDENCY_OVERRIDE for r in cdr.relations
    )
    assert composition_0002.identity.status.value in {"AVAILABLE", "PARTIAL"}
    assert composition_0002.career.status.value in {"AVAILABLE", "PARTIAL"}
    assert "Tôi là ai" in composition_0002.identity.body
    assert "Phong cách làm việc" in composition_0002.career.body
    assert "TRUE_CONFLICT" not in composition_0002.executive.body
    assert "claim_id" not in composition_0002.executive.body
    assert "DEPENDENCY_OVERRIDE" not in composition_0002.executive.body


def test_case_0001_regression(composition_0001) -> None:
    strength = composition_0001.domains["strength"]
    assert strength.diagnostics.get("class_id") in {"strong", "very_strong"} or (
        "vượng" in strength.conclusion.lower() or "nội lực" in strength.conclusion.lower()
    )
    assert "Chính Ấn" in composition_0001.domains["pattern"].conclusion
    assert composition_0001.executive.status.value in {"AVAILABLE", "PARTIAL"}
    assert "Bạn là ai" in composition_0001.executive.body
    assert composition_0001.identity.status.value in {"AVAILABLE", "PARTIAL"}
    assert composition_0001.career.status.value in {"AVAILABLE", "PARTIAL"}


def test_second_case_determinism(engine_synth) -> None:
    service = MultiDomainInterpretationService()
    a = service.compose(case_id="SYNTHETIC-B", engine_output=engine_synth)
    b = service.compose(case_id="SYNTHETIC-B", engine_output=engine_synth)
    assert a.cross_domain.to_validation_dict() == b.cross_domain.to_validation_dict()
    assert a.executive.body == b.executive.body
    assert a.identity.body == b.identity.body


def test_generalization_divergence(composition_0001, composition_synth) -> None:
    assert (
        composition_0001.cross_domain.primary_theme
        != composition_synth.cross_domain.primary_theme
        or composition_0001.executive.body != composition_synth.executive.body
    )


def test_customer_mode_leak_prevention(tmp_path, composition_0002) -> None:
    result = ProductionEndToEndOrchestrator().run(CASE_0002_REQUEST)
    assert result.success is True
    payload = result.to_customer_dict()
    blob = json.dumps(payload, ensure_ascii=False)
    for token in (
        "TRUE_CONFLICT",
        "DEPENDENCY_OVERRIDE",
        "claim_id",
        "narrative_plan",
        "DRAFT_KNOWLEDGE",
    ):
        assert token not in blob or token in {
            # allow only if buried in domain text unlikely
        }
    assert "TRUE_CONFLICT" not in blob
    assert "DEPENDENCY_OVERRIDE" not in blob
    assert "claim_id" not in blob
    assert result.customer.section_status.identity_report.value in {
        "AVAILABLE",
        "PARTIAL",
    }
    assert result.customer.section_status.career_report.value in {
        "AVAILABLE",
        "PARTIAL",
    }
    assert result.customer.identity_report
    assert result.customer.career_report
    assert composition_0002.cross_domain.diagnostics.get("why_primary")


def test_identity_career_integration(composition_0001) -> None:
    assert "Mẫu vận hành" in composition_0001.identity.body
    assert "Hướng cân bằng" in composition_0001.career.body or (
        "cân bằng" in composition_0001.career.body.lower()
    )
