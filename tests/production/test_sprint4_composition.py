"""Sprint 4 multi-domain interpretation composition tests."""

from __future__ import annotations

import json

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.fixtures.case_0002_readiness import SYNTHETIC_REQUEST_B
from applications.production.interpretation.conflict_control import detect_conflicts
from applications.production.interpretation.contracts import DomainStatus
from applications.production.interpretation.duplicate_control import apply_duplicate_policy
from applications.production.interpretation.pattern_composer import (
    PatternDomainComposer,
    build_pattern_published_facts,
)
from applications.production.interpretation.service import MultiDomainInterpretationService
from applications.production.interpretation.strength_composer import StrengthDomainComposer
from applications.production.interpretation.ten_gods_composer import (
    TenGodsDomainComposer,
    build_ten_gods_published_facts,
)
from applications.production.interpretation.theme_keys import (
    THEME_ENDURANCE,
    THEME_OUTPUT_RELEASE,
)
from applications.production.interpretation.useful_god_composer import (
    UsefulGodDomainComposer,
    build_useful_god_published_facts,
)
from applications.production.interpretation.contracts import DomainClaim
from applications.production.master_reference import (
    load_golden_executive_for_comparison,
    load_golden_master_parts_for_comparison,
)
from applications.production.orchestrator import ProductionEndToEndOrchestrator


@pytest.fixture(scope="module")
def engine_a():
    return ProductionEngineRunner().run(CASE_0001_REQUEST)


@pytest.fixture(scope="module")
def engine_b():
    return ProductionEngineRunner().run(SYNTHETIC_REQUEST_B)


@pytest.fixture(scope="module")
def composition_a(engine_a):
    return MultiDomainInterpretationService().compose(
        case_id="CASE-0001",
        engine_output=engine_a,
    )


@pytest.fixture(scope="module")
def composition_b(engine_b):
    return MultiDomainInterpretationService().compose(
        case_id="SYNTHETIC-B",
        engine_output=engine_b,
    )


def test_strength_generic_composition(engine_a) -> None:
    result = StrengthDomainComposer().compose(
        case_id="CASE-0001",
        strength_result=engine_a.strength_result,
        strength_context=engine_a.strength_context,
    )
    assert result.status == DomainStatus.AVAILABLE
    assert "vượng" in result.conclusion.lower() or "nội lực" in result.conclusion.lower()
    assert result.knowledge_status.value == "DRAFT_KNOWLEDGE"
    customer = result.to_customer_dict()
    assert "diagnostics" not in customer
    assert "claims" not in customer


def test_ten_gods_generic_composition(engine_a) -> None:
    facts = build_ten_gods_published_facts(engine_a.ten_gods)
    result = TenGodsDomainComposer().compose(facts)
    assert result.status in {DomainStatus.AVAILABLE, DomainStatus.PARTIAL}
    assert "Thập Thần" in result.conclusion or "vai trò" in result.conclusion
    assert "Tỷ Kiên là" not in result.conclusion  # not textbook definition dump


def test_pattern_generic_composition(engine_a) -> None:
    facts = build_pattern_published_facts(engine_a.analysis.pattern)
    result = PatternDomainComposer().compose(facts)
    assert result.status in {DomainStatus.AVAILABLE, DomainStatus.PARTIAL}
    assert "Chính Ấn" in result.conclusion
    assert "nội lực" not in result.conclusion.lower() or "không phải mô tả nội lực" in result.conclusion


def test_useful_god_generic_composition(engine_a) -> None:
    facts = build_useful_god_published_facts(engine_a.analysis.useful_god)
    result = UsefulGodDomainComposer().compose(facts)
    assert result.status == DomainStatus.AVAILABLE
    assert "Chính Quan" in result.conclusion
    assert result.recommendations


def test_domain_result_serialization_hides_internals(composition_a) -> None:
    for result in composition_a.domains.values():
        customer = result.to_customer_dict()
        forbidden = {"diagnostics", "claims", "knowledge_status", "matched_rules"}
        assert forbidden.isdisjoint(customer.keys())
        validation = result.to_validation_dict()
        assert "diagnostics" in validation
        assert "knowledge_status" in validation


def test_duplicate_control() -> None:
    claims = [
        DomainClaim("a", THEME_ENDURANCE, "sức bền A", "strength"),
        DomainClaim("b", THEME_ENDURANCE, "sức bền B", "ten_gods"),
        DomainClaim("c", THEME_OUTPUT_RELEASE, "tiết khí", "useful_god"),
        DomainClaim("d", THEME_OUTPUT_RELEASE, "tiết khí lại", "strength"),
    ]
    kept, suppressed = apply_duplicate_policy(claims)
    assert len(kept) == 2
    assert "b" in suppressed
    assert "d" in suppressed
    endurance = next(item for item in kept if item.theme_id == THEME_ENDURANCE)
    assert endurance.domain == "strength"


def test_conflict_control(composition_a) -> None:
    conflicts = detect_conflicts(composition_a.domains)
    assert isinstance(conflicts, list)
    for conflict in conflicts:
        assert conflict.classification.value in {
            "TRUE_CONFLICT",
            "CONDITIONAL_NUANCE",
            "DIFFERENT_SCOPE",
        }


def test_executive_consulting_generic(composition_a) -> None:
    executive = composition_a.executive
    assert executive.status in {DomainStatus.AVAILABLE, DomainStatus.PARTIAL}
    assert "Bạn là ai" in executive.body
    assert "Ba ưu tiên" in executive.body
    assert "PART_08" not in executive.body
    golden = load_golden_executive_for_comparison("CASE-0001")
    assert golden[:120] not in executive.body


def test_case_0001_golden_comparison_direction(composition_a) -> None:
    """Compare claim direction to golden masters — not word-for-word."""
    parts = load_golden_master_parts_for_comparison("CASE-0001")
    strength = composition_a.domains["strength"]
    useful = composition_a.domains["useful_god"]
    pattern = composition_a.domains["pattern"]
    assert strength.diagnostics["class_id"] == "strong"
    assert "Chính Quan" in useful.conclusion
    assert "Chính Ấn" in pattern.conclusion
    # Golden masters remain reference; generic must not copy Part 08 opening.
    assert "# 1. Bạn là ai\n\nBạn là người được xây trên" not in (
        composition_a.executive.body
    )
    assert "Part 01" not in strength.conclusion
    assert len(parts["01"]) > 200


def test_second_request_divergence(composition_a, composition_b) -> None:
    assert composition_a.domains["useful_god"].conclusion != (
        composition_b.domains["useful_god"].conclusion
    )
    assert composition_a.domains["pattern"].conclusion != (
        composition_b.domains["pattern"].conclusion
    )
    assert composition_a.executive.body != composition_b.executive.body


def test_no_case_0001_prose_in_synthetic(composition_b) -> None:
    payload = json.dumps(composition_b.customer_domain_payloads(), ensure_ascii=False)
    assert "Nguyễn Tiến Sơn" not in payload
    golden = load_golden_executive_for_comparison("CASE-0001")
    assert golden[200:400] not in composition_b.executive.body


def test_missing_data_restraint(engine_a) -> None:
    facts = build_useful_god_published_facts({"useful_god": "", "favorable_gods": []})
    result = UsefulGodDomainComposer().compose(facts)
    assert result.status == DomainStatus.INSUFFICIENT
    assert result.conclusion == ""
    assert not result.sections


def test_determinism_composition(engine_a) -> None:
    service = MultiDomainInterpretationService()
    first = service.compose(case_id="CASE-0001", engine_output=engine_a)
    second = service.compose(case_id="CASE-0001", engine_output=engine_a)
    assert first.executive.body == second.executive.body
    assert first.domains["ten_gods"].conclusion == second.domains["ten_gods"].conclusion


def test_orchestrator_customer_mode_no_leak(tmp_path) -> None:
    result = ProductionEndToEndOrchestrator().run_case_0001(export_dir=tmp_path)
    assert result.success is True
    payload = result.to_customer_dict()
    forbidden = {
        "diagnostics",
        "knowledge_status",
        "claims",
        "narrative_plan",
        "matched_rules",
        "DRAFT_KNOWLEDGE",
        "catalog_is_draft",
    }
    blob = json.dumps(payload, ensure_ascii=False)
    for key in forbidden:
        assert key not in payload
        if key in {"DRAFT_KNOWLEDGE", "catalog_is_draft"}:
            assert key not in blob
    assert result.customer.master_interpretation_parts == {}
    assert result.customer.section_status.executive_consulting.value in {
        "AVAILABLE",
        "PARTIAL",
    }
    assert "Bạn là ai" in result.customer.executive_consulting
