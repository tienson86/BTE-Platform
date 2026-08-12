"""Commercial Language Layer V1.2 tests."""

from __future__ import annotations

import json

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.fixtures.case_0002_readiness import CASE_0002_REQUEST
from applications.production.interpretation.service import MultiDomainInterpretationService
from applications.production.language.models import (
    CommercialLanguageInput,
    FeatureKind,
    ParagraphIntent,
)
from applications.production.language import plain_language as pl
from applications.production.language.service import CommercialLanguageService
from applications.production.language.writer import realize_paragraph


FORBIDDEN = (
    "align_operating_role:",
    "apply_balance:",
    "balance:",
    "body:",
    "structure:",
    "avoid_reflex_extra_load",
    "TRUE_CONFLICT",
    "DEPENDENCY_OVERRIDE",
    "OPERATING_OUTPUT",
    "FOLLOW_STRUCTURE",
    "claim_id",
)


@pytest.fixture(scope="module")
def composition_0001():
    engine = ProductionEngineRunner().run(CASE_0001_REQUEST)
    return MultiDomainInterpretationService().compose(
        case_id="CASE-0001",
        engine_output=engine,
    )


@pytest.fixture(scope="module")
def composition_0002():
    engine = ProductionEngineRunner().run(CASE_0002_REQUEST)
    return MultiDomainInterpretationService().compose(
        case_id="CASE-0002",
        engine_output=engine,
    )


def test_plain_language_mapping() -> None:
    assert "đầu ra" in pl.plain_theme("OPERATING_OUTPUT")
    assert "biểu đạt" in pl.plain_style("Thương Quan")
    assert "cân bằng" in pl.plain_capacity("balanced") or "nhịp" in pl.plain_capacity("balanced")
    assert "Đừng nhận thêm" in pl.plain_avoid("avoid_reflex_extra_load")
    action = pl.plain_priority("align_operating_role:Thương Quan")
    assert "align_operating_role" not in action
    assert "biểu đạt" in action or "đầu ra" in action


def test_deterministic_pattern_selection() -> None:
    data = CommercialLanguageInput(
        feature=FeatureKind.IDENTITY,
        section="WHO",
        intent=ParagraphIntent.OBSERVATION,
        claims=["identity_core"],
        primary_theme="OPERATING_OUTPUT",
        operating_style="Thương Quan",
        capacity_cue="balanced",
        structure_cue="Tòng Nhi",
    )
    a = realize_paragraph(data)
    b = realize_paragraph(data)
    assert a.prose == b.prose
    assert a.prose.startswith("Điểm nhận diện") or "Điểm nhận diện" in a.prose
    assert not a.prose.startswith("Bạn ")


def test_paragraph_traceability() -> None:
    data = CommercialLanguageInput(
        feature=FeatureKind.CAREER,
        section="FOCUS",
        intent=ParagraphIntent.ACTION,
        claims=["align_operating_role:Thương Quan"],
        actionability="align_operating_role:Thương Quan",
    )
    paragraph = realize_paragraph(data)
    assert "align_operating_role:Thương Quan" in paragraph.source_claim_ids
    assert paragraph.action
    assert "align_operating_role" not in paragraph.prose


def test_action_traceability() -> None:
    text = pl.plain_priority("keep_load_recovery_rhythm")
    assert "tải" in text.lower() or "phục hồi" in text.lower()
    assert "cần cân bằng" != text


def test_no_claim_key_or_enum_leak(composition_0002) -> None:
    for body in (
        composition_0002.identity.body,
        composition_0002.career.body,
        composition_0002.executive.body,
    ):
        for token in FORBIDDEN:
            assert token not in body, token
        assert composition_0002.identity.diagnostics["cll"]["leak_free"] is True


def test_identity_composition_sections(composition_0002) -> None:
    ids = {s.section_id for s in composition_0002.identity.sections}
    for required in {
        "WHO",
        "OPERATING",
        "STRENGTHS",
        "BLIND_SPOTS",
        "PRESSURE",
        "ENVIRONMENT",
        "LESSON",
        "ACTIONS",
        "SUMMARY",
    }:
        assert required in ids
    assert "Tôi là ai" in composition_0002.identity.body
    assert "chuẩn mực" not in composition_0002.identity.body.lower() or (
        "không" in composition_0002.identity.body.lower()
    )


def test_career_authority_not_generic_standards(composition_0002) -> None:
    body = composition_0002.career.body
    assert "Tư thế vai trò" in body or "POSTURE" in {
        s.section_id for s in composition_0002.career.sections
    }
    assert "Áp lực chuẩn mực / trách nhiệm là một tín hiệu" not in body
    assert "đầu ra" in body.lower() or "biểu đạt" in body.lower()
    assert "chức danh" not in body.lower()
    assert "thu nhập" not in body.lower()


def test_executive_one_voice(composition_0002) -> None:
    body = composition_0002.executive.body
    assert "Bạn là ai" in body
    assert "Ba ưu tiên" in body
    assert "balance:" not in body
    assert "gánh thêm vô hạn" not in body


def test_case_0002_acceptance(composition_0002) -> None:
    cdr = composition_0002.cross_domain
    assert cdr.primary_theme == "OPERATING_OUTPUT"
    assert cdr.tensions
    blob = "\n".join(
        [
            composition_0002.identity.body,
            composition_0002.career.body,
            composition_0002.executive.body,
        ]
    )
    for token in FORBIDDEN:
        assert token not in blob
    # Nuance preserved in lived language
    assert "hai" in blob.lower() and (
        "khía cạnh" in blob.lower() or "điều kiện" in blob.lower() or "khung" in blob.lower()
    )
    mem_i = composition_0002.identity.diagnostics.get("memory_line", "")
    mem_c = composition_0002.career.diagnostics.get("memory_line", "")
    assert mem_i
    assert mem_c


def test_case_0001_regression(composition_0001) -> None:
    assert composition_0001.cross_domain.primary_theme == "OPERATING_SELF_CARRY"
    assert composition_0001.domains["strength"].diagnostics.get("class_id") in {
        "strong",
        "very_strong",
        None,
    } or "nội lực" in composition_0001.domains["strength"].conclusion.lower()
    assert "Chính Ấn" in composition_0001.domains["pattern"].conclusion
    assert composition_0001.identity.status.value in {"AVAILABLE", "PARTIAL"}
    assert composition_0001.career.status.value in {"AVAILABLE", "PARTIAL"}
    assert "Bạn là ai" in composition_0001.executive.body
    assert "gánh thêm vô hạn" not in composition_0001.executive.body  # no old stitch required
    # Meaning aligned: self-carry / capacity language present
    blob = composition_0001.identity.body + composition_0001.executive.body
    assert "tự" in blob.lower() or "gánh" in blob.lower() or "chịu tải" in blob.lower()


def test_cross_case_language_divergence(composition_0001, composition_0002) -> None:
    assert composition_0001.identity.body != composition_0002.identity.body
    assert composition_0001.career.body != composition_0002.career.body
    assert composition_0001.executive.body != composition_0002.executive.body
    m1 = composition_0001.identity.diagnostics.get("memory_line", "")
    m2 = composition_0002.identity.diagnostics.get("memory_line", "")
    assert m1 != m2


def test_memory_line_uniqueness(composition_0001, composition_0002) -> None:
    assert (
        composition_0001.executive.diagnostics.get("memory_line")
        != composition_0002.executive.diagnostics.get("memory_line")
    )


def test_missing_data_restraint() -> None:
    data = CommercialLanguageInput(
        feature=FeatureKind.IDENTITY,
        section="WHO",
        intent=ParagraphIntent.OBSERVATION,
    )
    paragraph = realize_paragraph(data)
    assert paragraph.status.value == "INSUFFICIENT"
    assert "Chưa đủ dữ liệu" in paragraph.prose


def test_determinism_cll(composition_0002) -> None:
    engine = ProductionEngineRunner().run(CASE_0002_REQUEST)
    service = MultiDomainInterpretationService()
    a = service.compose(case_id="CASE-0002", engine_output=engine)
    b = service.compose(case_id="CASE-0002", engine_output=engine)
    assert a.identity.body == b.identity.body
    assert a.career.body == b.career.body
    assert a.executive.body == b.executive.body


def test_service_leak_diagnostics(composition_0002) -> None:
    assert composition_0002.identity.diagnostics["cll"]["cll_version"] == "1.2.0"
    assert composition_0002.career.diagnostics["cll"]["leak_free"] is True
    assert composition_0002.executive.diagnostics["cll"]["leak_free"] is True
