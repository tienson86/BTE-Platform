"""Generic production pipeline tests — Sprint 3."""

from __future__ import annotations

import json

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.fixtures.case_0002_readiness import SYNTHETIC_REQUEST_B
from applications.production.master_reference import load_golden_executive_for_comparison
from applications.production.models import EXECUTIVE_CONSULTING_NOT_AVAILABLE, ProductionRequest
from applications.production.orchestrator import ProductionEndToEndOrchestrator


def _request_without_case_id(request: ProductionRequest, export_dir) -> ProductionRequest:
    return ProductionRequest(
        year=request.year,
        month=request.month,
        day=request.day,
        hour=request.hour,
        minute=request.minute,
        gender=request.gender,
        timezone=request.timezone,
        full_name=request.full_name,
        birth_place=request.birth_place,
        case_id="",
        export_pdf=True,
        export_dir=export_dir,
    )


@pytest.fixture(scope="module")
def generic_result_a(tmp_path_factory):
    export_dir = tmp_path_factory.mktemp("generic_a")
    request = _request_without_case_id(CASE_0001_REQUEST, export_dir)
    return ProductionEndToEndOrchestrator().run(request)


@pytest.fixture(scope="module")
def generic_result_b():
    return ProductionEndToEndOrchestrator().run(SYNTHETIC_REQUEST_B)


def test_generic_engine_runner_accepts_request() -> None:
    """ProductionEngineRunner runs without CASE-0001 branching."""
    output = ProductionEngineRunner().run(SYNTHETIC_REQUEST_B)
    assert "calendar" in output.stages
    assert "bazi" in output.stages
    assert "strength" in output.stages
    assert output.strength_result.success is True


def test_two_distinct_requests_run(generic_result_a, generic_result_b) -> None:
    """Two distinct generic requests complete without CASE-0001 hard-coding."""
    assert generic_result_a.success is True
    assert generic_result_b.success is True
    assert generic_result_a.case_id != generic_result_b.case_id


def test_no_case_0001_prose_leakage(generic_result_b) -> None:
    """Generic cases never receive CASE-0001 master prose."""
    customer = generic_result_b.customer
    assert customer.master_interpretation_parts == {}
    golden_exec = load_golden_executive_for_comparison("CASE-0001")
    assert golden_exec[:200] not in customer.executive_consulting
    assert "# CASE-0001 MASTER CONSULTING REPORT" not in customer.executive_consulting
    payload = json.dumps(customer.to_dict(), ensure_ascii=False)
    assert "Nguyễn Tiến Sơn" not in payload


def test_executive_consulting_generic_available(generic_result_a) -> None:
    """Executive consulting is generated generically — not Part 08 markdown."""
    status = generic_result_a.customer.section_status.executive_consulting.value
    assert status in {"AVAILABLE", "PARTIAL"}
    assert "Bạn là ai" in generic_result_a.customer.executive_consulting
    assert generic_result_a.customer.executive_consulting != EXECUTIVE_CONSULTING_NOT_AVAILABLE


def test_strength_interpretation_available(generic_result_a) -> None:
    """Strength domain produces customer sections via generic composition."""
    assert (
        generic_result_a.customer.section_status.strength_interpretation.value
        == "AVAILABLE"
    )
    sections = generic_result_a.customer.strength_interpretation.get("sections", [])
    assert len(sections) >= 1


def test_determinism_generic_pipeline() -> None:
    """Same generic request yields identical strength classification."""
    first = ProductionEngineRunner().run(SYNTHETIC_REQUEST_B)
    second = ProductionEngineRunner().run(SYNTHETIC_REQUEST_B)
    assert first.strength_result.strength_level == second.strength_result.strength_level
    assert first.strength_result.strength_score == second.strength_result.strength_score


def test_customer_mode_hides_diagnostics(generic_result_a) -> None:
    """Customer payload excludes diagnostics and knowledge status."""
    payload = generic_result_a.to_customer_dict()
    forbidden = {
        "diagnostics",
        "knowledge",
        "validation_mode",
        "narrative_plan",
        "dayun_sequence",
        "catalog_is_draft",
    }
    assert forbidden.isdisjoint(payload.keys())
    assert "diagnostics" not in json.dumps(payload)


def test_diagnostics_expose_knowledge_status(generic_result_a) -> None:
    """Diagnostics expose Draft catalog status — not customer-visible."""
    knowledge = generic_result_a.diagnostics["knowledge"]
    assert knowledge["catalog_is_draft"] is True
    assert "Draft" in knowledge["catalog_statuses"]


def test_diagnostics_retain_luck_sequence(generic_result_a) -> None:
    """Internal diagnostics retain full DaYun sequence without public API change."""
    luck = generic_result_a.diagnostics["luck_internal"]
    assert luck["dayun_sequence_count"] >= 1
    assert isinstance(luck["dayun_sequence"], list)
