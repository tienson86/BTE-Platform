"""TV1-B06 public API create/get/validation tests."""

from __future__ import annotations

import inspect
import json
import re

from fastapi.testclient import TestClient

from consulting.marriage.api import http as http_module
from consulting.marriage.api import service as service_module
from consulting.marriage.api.http import create_marriage_api_app
from consulting.marriage.api.placeholder import PlaceholderMarriageApi
from consulting.marriage.api.service import MarriageConsultationApi
from consulting.marriage.api.versions import API_VERSION
from consulting.marriage.runtime.narrative_wiring import wire_marriage_report_runtime
from tests.consulting.api_fixtures import api_client, valid_body


def test_post_valid_consultation() -> None:
    """POST creates a SUCCESS consultation resource."""
    client, _ = api_client()
    response = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "SUCCESS"
    data = payload["data"]
    assert data["consultation_id"].startswith("MC-")
    assert data["score"] is None
    assert data["grade"] is None
    assert data["overall_state"]
    assert payload["version_bundle"]["api_version"] == API_VERSION


def test_person_a_b_validation_and_missing_gender() -> None:
    """Both persons are required. Missing gender is rejected without defaulting."""
    client, _ = api_client()
    missing = valid_body()
    del missing["person_b"]
    response = client.post("/api/v1/consulting/marriage", json=missing)
    assert response.status_code == 400
    assert response.json()["status"] == "FAILED"
    no_gender = valid_body(gender_a=None)
    response = client.post("/api/v1/consulting/marriage", json=no_gender)
    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "FAILED"
    assert body["errors"][0]["code"] == "VALIDATION_ERROR"
    assert "gender" in body["errors"][0]["message"]


def test_missing_birth_time_accepted() -> None:
    """Unknown birth time is allowed and surfaces as a warning, not marital risk."""
    client, _ = api_client()
    response = client.post("/api/v1/consulting/marriage", json=valid_body(time_a=None, time_b=None))
    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "SUCCESS"
    codes = [item["code"] for item in payload["warnings"]]
    assert "BIRTH_TIME_UNKNOWN" in codes
    assert all("marital" not in item["description"].lower() or "not a marital" in item["description"].lower() for item in payload["warnings"] if item["code"] == "BIRTH_TIME_UNKNOWN")


def test_invalid_date_rejected() -> None:
    """Invalid birth dates are validation failures."""
    client, _ = api_client()
    response = client.post(
        "/api/v1/consulting/marriage",
        json=valid_body(birth_date_a="1987-13-40"),
    )
    assert response.status_code == 400
    assert response.json()["status"] == "FAILED"


def test_no_default_gender_or_time() -> None:
    """Omitted time stays omitted. Omitted gender is not filled in."""
    client, _ = api_client()
    response = client.post("/api/v1/consulting/marriage", json=valid_body(gender_b=None, time_b=None))
    assert response.status_code == 400
    response = client.post("/api/v1/consulting/marriage", json=valid_body(time_b=None))
    assert response.status_code == 201
    codes = [item["code"] for item in response.json()["warnings"]]
    assert "BIRTH_TIME_UNKNOWN" in codes


def test_consultation_summary_report_get() -> None:
    """GET consultation, summary, and report share the same consultation_id."""
    client, _ = api_client()
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    consultation_id = created["consultation_id"]
    got = client.get(f"/api/v1/consulting/marriage/{consultation_id}")
    assert got.status_code == 200
    assert got.json()["data"]["consultation_id"] == consultation_id
    summary = client.get(f"/api/v1/consulting/marriage/{consultation_id}/summary")
    assert summary.status_code == 200
    summary_data = summary.json()["data"]
    assert summary_data["consultation_id"] == consultation_id
    assert "headline" in summary_data
    assert "top_strengths" in summary_data
    assert "top_risks" in summary_data
    assert "top_action_themes" in summary_data
    assert summary_data["score"] is None
    report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report")
    assert report.status_code == 200
    sections = [item["section_id"] for item in report.json()["data"]["sections"]]
    assert sections[0] == "identity"
    assert "compatibility_hero" in sections
    assert report.json()["data"]["score"] is None
    assert report.json()["data"]["grade"] is None


def test_not_found_behavior() -> None:
    """Unknown consultation ids return HTTP 404 and business FAILED."""
    client, _ = api_client()
    response = client.get("/api/v1/consulting/marriage/MC-19990101-XXXXXX")
    assert response.status_code == 404
    assert response.json()["status"] == "FAILED"
    assert response.json()["errors"][0]["code"] == "NOT_FOUND"


def test_customer_dto_hides_internal_ids() -> None:
    """Customer JSON must not expose Evidence/Finding/Rule ids."""
    client, _ = api_client()
    consultation_id = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]["consultation_id"]
    for path in (
        f"/api/v1/consulting/marriage/{consultation_id}",
        f"/api/v1/consulting/marriage/{consultation_id}/summary",
        f"/api/v1/consulting/marriage/{consultation_id}/report",
    ):
        text = json.dumps(client.get(path).json()["data"])
        assert not re.search(r"\bEV-\d{4}\b", text)
        assert not re.search(r"\bF-\d{4}\b", text)
        assert "source_finding_ids" not in text
        assert "canonical analysis" not in text.lower()


def test_expert_mode_controlled_trace() -> None:
    """Expert query returns finding references without changing Decision."""
    client, _ = api_client()
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    consultation_id = created["consultation_id"]
    customer_state = created["overall_state"]
    expert = client.get(f"/api/v1/consulting/marriage/{consultation_id}?expert=true")
    assert expert.status_code == 200
    data = expert.json()["data"]
    assert data["overall_state"] == customer_state
    assert data["score"] is None
    refs = data["expert"]["finding_references"]
    assert refs
    assert "finding_id" in refs[0]
    report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report?expert=true").json()["data"]
    assert any("source_finding_ids" in json.dumps(block) for section in report["sections"] for block in section["blocks"])


def test_warning_and_error_serialization() -> None:
    """Warnings and errors use the public envelope, not Python tracebacks."""
    client, _ = api_client()
    failed = client.post("/api/v1/consulting/marriage", json=valid_body(gender_a=None))
    error = failed.json()["errors"][0]
    assert set(error) >= {"code", "stage", "message", "retryable"}
    assert "traceback" not in json.dumps(failed.json()).lower()
    ok = client.post("/api/v1/consulting/marriage", json=valid_body(time_a=None))
    warning = ok.json()["warnings"][0]
    assert set(warning) >= {"code", "description"}


def test_api_version_independent_from_decision() -> None:
    """API v1 stays independent from marriage policy version."""
    client, _ = api_client()
    payload = client.post("/api/v1/consulting/marriage", json=valid_body()).json()
    versions = payload["version_bundle"]
    assert versions["api_version"] == "v1"
    assert versions["policy_version"] != versions["api_version"]
    assert versions["policy_version"].startswith("marriage.policy")


def test_no_route_side_narrative_or_decision() -> None:
    """Routes and API service do not compose catalog wording or mutate Decision."""
    http_src = inspect.getsource(http_module)
    service_src = inspect.getsource(service_module)
    assert "overall_entry" not in http_src
    assert "CanonicalNarrativeComposer" not in http_src
    assert "CanonicalRecommendationProvider" not in http_src
    assert "overall_entry" not in service_src


def test_healthz_is_available() -> None:
    """Marriage API process exposes a non-semantic liveness route."""
    _client, container = api_client()
    response = TestClient(create_marriage_api_app(container)).get("/healthz")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "tv01-marriage-api"


def test_b05_wiring_still_placeholder_api() -> None:
    """Frozen B05 factory does not bind the public API implementation."""
    container = wire_marriage_report_runtime()
    assert isinstance(container.api_contract, PlaceholderMarriageApi)
    assert not isinstance(container.api_contract, MarriageConsultationApi)
