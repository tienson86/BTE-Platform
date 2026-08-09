"""Integration tests validating ReportResponse against frozen JSON Schema."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

from applications.api.app import create_app

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    PROJECT_ROOT / "applications" / "api" / "schemas" / "report_response.schema.json"
)

VALID_ANALYZE_REQUEST: dict[str, object] = {
    "request_id": "integration-schema-001",
    "api_version": "1.0.0",
    "language": "vi",
    "chart": {
        "year": 1990,
        "month": 5,
        "day": 15,
        "hour": 10,
        "minute": 30,
        "gender": "male",
        "timezone": "Asia/Ho_Chi_Minh",
    },
    "report_template": "standard",
    "options": {},
}


@pytest.fixture(scope="module")
def report_schema() -> dict[str, object]:
    """Load the frozen ReportResponse JSON Schema."""
    with SCHEMA_PATH.open(encoding="utf-8") as handle:
        schema = json.load(handle)
    assert isinstance(schema, dict)
    return schema


@pytest.fixture(scope="module")
def schema_validator(report_schema: dict[str, object]) -> Draft202012Validator:
    """Build a Draft 2020-12 validator for ReportResponse."""
    Draft202012Validator.check_schema(report_schema)
    return Draft202012Validator(report_schema)


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Return a FastAPI test client shared for schema tests."""
    return TestClient(create_app())


@pytest.fixture(scope="module")
def successful_analysis_response(client: TestClient) -> dict[str, object]:
    """Capture one successful analysis response for schema validation."""
    response = client.post("/analysis", json=VALID_ANALYZE_REQUEST)
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, dict)
    return payload


def test_report_response_schema_file_exists() -> None:
    """Frozen schema file must exist."""
    assert SCHEMA_PATH.is_file()


def test_report_response_schema_is_valid(report_schema: dict[str, object]) -> None:
    """Frozen schema must be a valid Draft 2020-12 document."""
    Draft202012Validator.check_schema(report_schema)
    assert report_schema.get("title") == "BTE ReportResponse"


def test_successful_analysis_matches_frozen_schema(
    successful_analysis_response: dict[str, object],
    schema_validator: Draft202012Validator,
) -> None:
    """Every successful analysis response must pass schema validation."""
    errors = sorted(
        schema_validator.iter_errors(successful_analysis_response),
        key=lambda error: list(error.path),
    )
    assert errors == [], "; ".join(
        f"{list(error.path)}: {error.message}" for error in errors
    )


def test_successful_analysis_required_sections_present(
    successful_analysis_response: dict[str, object],
) -> None:
    """Schema-required top-level sections must be present."""
    required = {
        "metadata",
        "chart",
        "analysis",
        "interpretation",
        "report",
        "diagnostics",
    }
    assert required.issubset(successful_analysis_response.keys())
