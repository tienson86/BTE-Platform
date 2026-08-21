"""G2-06 end-to-end customer acceptance (API + stored export path)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from applications.api.app import app
from applications.api.exceptions import CustomerExportError
from applications.api.services.customer_contract import CONTRACT_MISMATCH_MESSAGE
from applications.api.services.customer_export import prepare_customer_report_input

PROBE = Path(__file__).resolve().parents[3] / "release" / "gate_02" / "G2_06_E2E_PROBE.json"


def test_invalid_analyze_is_recoverable_and_creates_no_result() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/analyze", json={"year": 0, "month": 5, "day": 15})
    assert response.status_code == 422
    assert "Traceback" not in response.text
    body = response.json()
    assert body.get("success") is not True


def test_stale_contract_export_is_blocked() -> None:
    with pytest.raises(CustomerExportError) as caught:
        prepare_customer_report_input(
            analysis_id="old",
            source="history",
            data={"analysis_id": "old", "pattern": {"dung_than": "Thủy", "hy_than": "Kim"}},
        )
    assert caught.value.status_code == 409
    assert CONTRACT_MISMATCH_MESSAGE in caught.value.message


def test_pattern_evidence_does_not_expose_rule_ids() -> None:
    report = prepare_customer_report_input(
        analysis_id="son",
        source="current",
        data={
            "analysis_id": "son",
            "useful_god_source": {"contract": "analysis_result.UsefulGodView@1.5"},
            "useful_god": {
                "useful_display": "Hỏa · Đinh · Chính Quan",
                "favorable_display": "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng",
            },
            "pattern": {
                "cach_cuc": "Chính Ấn",
                "evidence_compact": "Nguyệt lệnh Sửu · rule pat_ca_01",
            },
            "bazi": {},
        },
        birth_input={"name": "Nguyễn Tiến Sơn", "year": 1987, "month": 1, "day": 21},
    )
    assert "pat_ca_01" not in (report.pattern.explanation or "")
    assert "rule " not in (report.pattern.explanation or "").lower()
    assert "Chính Ấn" == report.pattern.primary_pattern


def test_g2_06_probe_artifacts_are_complete() -> None:
    if not PROBE.is_file():
        pytest.skip("run python release/gate_02/_g2_06_e2e_probe.py first")
    payload = json.loads(PROBE.read_text(encoding="utf-8"))
    assert payload["mismatch_count"] == 0
    assert payload["ten_match"] is True
    assert all(status == "PASS" for status in payload["primary_journeys"].values())
    assert payload["history"]["ok"] is True
    assert all(payload["cross_files"].values())
    assert all(row["coherent"] for row in payload["id_trace"])
