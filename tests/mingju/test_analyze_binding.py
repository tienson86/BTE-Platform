"""Live analyze integration: MC-01 binds without leaking debug metadata."""

from __future__ import annotations

from fastapi.testclient import TestClient

from applications.api.app import create_app
from engines.mingju.enums import PatternGrade


def test_fresh_analyze_binds_mc01_without_score_grade() -> None:
    client = TestClient(create_app())
    body = {
        "year": 1987,
        "month": 1,
        "day": 21,
        "hour": 4,
        "minute": 30,
        "gender": "male",
        "full_name": "Nguyễn Tiến Sơn",
        "birth_place": "Hà Nội",
    }
    analyzed = client.post("/api/v1/analyze", json=body)
    assert analyzed.status_code == 200
    data = analyzed.json()["data"]
    assert "mc01" not in data
    assert "mingju" not in data
    pattern = data.get("pattern") or {}
    assert pattern.get("cach_cuc")
    assert pattern.get("structural_grade") in {item.value for item in PatternGrade if item.value != "UNRESOLVED"}
    assert pattern.get("structural_grade") != (data.get("score") or {}).get("grade")
    assert pattern.get("structural_purity")
    assert pattern.get("structural_integrity")
    diagnostics = client.post("/api/v1/dev/pack07/diagnostics", json=body)
    assert diagnostics.status_code == 200
    report = diagnostics.json()["data"]
    assert report["mc01_reference"] == "PASS"
    assert report["mc01_reference"] != "NOT_BOUND"
