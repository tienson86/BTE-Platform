"""Case management + export + analyze tests."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from applications.case_management.exporter import CaseExporter
from applications.case_management.models import CaseModel
from applications.case_management.repository import CaseRepository
from applications.case_management.service import (
    CaseNotFoundError,
    CaseService,
)
from applications.customer.repository import CustomerRepository
from applications.customer.service import CustomerService


def _fake_analyze(**kwargs: Any) -> dict[str, Any]:
    return {
        "pipeline": [
            "calendar",
            "bazi",
            "pattern",
            "score",
            "interpretation",
            "report",
            "narrative",
        ],
        "calendar": {"ok": True, "year": kwargs["year"]},
        "bazi": {"day_master": "Jia"},
        "pattern": {"patterns": []},
        "score": {"total": 80},
        "interpretation": {"summary": "demo", "sentence_count": 3},
        "report": {
            "title": "Report",
            "html": "<p>report</p>",
            "markdown": "# Report",
        },
        "narrative": {
            "title": "Narrative",
            "html": "<p>narrative</p>",
            "markdown": "# Narrative",
        },
    }


def _case_service(tmp_path: Path) -> CaseService:
    customers = CustomerService(CustomerRepository(tmp_path / "customers.json"))
    cases = CaseRepository(tmp_path / "cases.json")
    return CaseService(
        cases,
        customers,
        analyze_fn=_fake_analyze,
        engine_version="test-1.0",
    )


def test_case_crud_and_history(tmp_path: Path) -> None:
    service = _case_service(tmp_path)
    customer = service.customer_service.create(
        full_name="Case Owner",
        birth_datetime="1990-05-15T10:30:00",
        gender="female",
    )
    case = CaseModel.create(
        customer_id=customer.customer_id,
        engine_version="test",
        interpretation_result={"summary": "s1"},
    )
    service.create(case)
    assert service.get(case.case_id).customer_id == customer.customer_id
    history = service.history(customer.customer_id)
    assert len(history) == 1
    assert history[0]["case_id"] == case.case_id
    assert service.delete(case.case_id) is True
    with pytest.raises(CaseNotFoundError):
        service.get(case.case_id)


def test_analyze_customer_persists_case(tmp_path: Path) -> None:
    service = _case_service(tmp_path)
    customer = service.customer_service.create(
        full_name="Analyze Me",
        birth_datetime="1990-05-15T10:30:00",
        gender="male",
        timezone="Asia/Ho_Chi_Minh",
    )
    _, case, pipeline = service.analyze_customer(customer.customer_id)
    assert case.customer_id == customer.customer_id
    assert case.calendar_result["year"] == 1990
    assert pipeline["interpretation"]["summary"] == "demo"
    assert len(service.list(customer_id=customer.customer_id)) == 1


def test_case_exporter_formats() -> None:
    case = CaseModel.create(
        customer_id="c1",
        engine_version="1",
        interpretation_result={"summary": "hello"},
        report_result={"markdown": "# R", "html": "<b>R</b>"},
        narrative_result={"markdown": "# N", "html": "<b>N</b>"},
    )
    exporter = CaseExporter()
    assert '"case_id"' in exporter.to_json(case)
    assert "# Case" in exporter.to_markdown(case)
    assert "<html>" in exporter.to_html(case)
