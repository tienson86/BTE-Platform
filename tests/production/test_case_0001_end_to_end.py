"""Sprint 3/4 production end-to-end acceptance tests — generic pipeline."""

from __future__ import annotations

import pytest

from applications.production.models import SectionStatus
from applications.production.orchestrator import ProductionEndToEndOrchestrator
from engines.report_engine.exporting.pdf_exporter_v1 import validate_pdf_file


@pytest.fixture(scope="module")
def case_0001_e2e_result(tmp_path_factory):
    """Run CASE-0001 production pipeline once per module."""
    export_dir = tmp_path_factory.mktemp("case_0001_e2e")
    return ProductionEndToEndOrchestrator().run_case_0001(export_dir=export_dir)


def test_case_0001_e2e_success(case_0001_e2e_result) -> None:
    """CASE-0001 → one command → one report → PASS."""
    result = case_0001_e2e_result
    assert result.success is True
    assert result.errors == []
    assert result.pdf_path is not None
    assert result.pdf_path.is_file()
    validate_pdf_file(result.pdf_path)


def test_case_0001_all_stages_produce_output(case_0001_e2e_result) -> None:
    """Every pipeline stage completes without placeholder-only output."""
    required_stages = {
        "calendar",
        "bazi",
        "strength",
        "pattern",
        "useful_god",
        "ten_gods",
        "interpretation_v1",
        "interpretation_v2_strength",
        "interpretation_ten_gods",
        "interpretation_pattern",
        "interpretation_useful_god",
        "cross_domain_integration",
        "executive_consulting",
        "report_input_v1",
        "pdf_export",
    }
    completed = set(case_0001_e2e_result.stages_completed)
    missing = required_stages - completed
    assert not missing, f"Missing stages: {missing}"


def test_case_0001_customer_mode_hides_internals(case_0001_e2e_result) -> None:
    """Customer deliverable must not expose validation or trace fields."""
    payload = case_0001_e2e_result.to_customer_dict()
    forbidden = {
        "validation_mode",
        "narrative_plan",
        "diagnostics",
        "evidence",
        "trace",
        "reason_codes",
        "matched_rules",
        "rule_context",
        "internal",
        "luck",
        "knowledge",
        "catalog_is_draft",
    }
    assert forbidden.isdisjoint(payload.keys())
    strength = payload["strength_interpretation"]
    assert "validation_mode" not in strength
    assert "narrative_plan" not in strength
    assert "diagnostics" not in strength


def test_case_0001_no_master_prose_in_customer(case_0001_e2e_result) -> None:
    """Generic pipeline does not inject golden master markdown into customer output."""
    customer = case_0001_e2e_result.customer
    assert customer.master_interpretation_parts == {}
    assert customer.section_status.master_interpretation == SectionStatus.NOT_AVAILABLE
    assert "# CASE-0001 MASTER CONSULTING REPORT" not in customer.executive_consulting
    assert "Appendix A" not in customer.executive_consulting


def test_case_0001_strength_interpretation_customer_sections(
    case_0001_e2e_result,
) -> None:
    """Strength domain produces customer sections via generic composition."""
    sections = case_0001_e2e_result.customer.strength_interpretation.get(
        "sections", []
    )
    assert len(sections) >= 1
    for section in sections:
        assert section.get("body")
        assert "rule_id" not in section
    assert case_0001_e2e_result.customer.section_status.strength_interpretation in {
        SectionStatus.AVAILABLE,
        SectionStatus.PARTIAL,
    }


def test_case_0001_domain_and_executive_available(case_0001_e2e_result) -> None:
    """Sprint 4 domains and executive consulting are populated."""
    customer = case_0001_e2e_result.customer
    assert customer.ten_gods_interpretation.get("conclusion")
    assert customer.pattern_interpretation.get("conclusion")
    assert customer.useful_god_interpretation.get("conclusion")
    assert customer.section_status.executive_consulting in {
        SectionStatus.AVAILABLE,
        SectionStatus.PARTIAL,
    }
    assert len(customer.recommendations) >= 1
