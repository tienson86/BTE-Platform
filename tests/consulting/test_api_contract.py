"""TV1-B06 API contract, history, idempotency, and identity tests."""

from __future__ import annotations

import json

from consulting.marriage.api.versions import API_VERSION
from consulting.marriage.report.access import customer_sections
from tests.consulting.api_fixtures import api_client, api_service, valid_body

_CONSULTATION_FIELDS = {
    "consultation_id",
    "status",
    "created_at",
    "person_a",
    "person_b",
    "overall_state",
    "score",
    "grade",
    "confidence",
    "limitations",
    "versions",
    "headline",
    "action_themes",
}

_SUMMARY_FIELDS = {
    "consultation_id",
    "overall_state",
    "headline",
    "executive_summary",
    "top_strengths",
    "top_risks",
    "top_action_themes",
    "confidence",
    "limitations",
    "score",
    "grade",
}

_REPORT_FIELDS = {"consultation_id", "score", "grade", "metadata", "sections"}
_ENVELOPE_FIELDS = {"status", "data", "warnings", "errors", "version_bundle"}


def test_contract_field_names() -> None:
    """Public resources lock the frozen field names and nullable score/grade."""
    client, _ = api_client()
    payload = client.post("/api/v1/consulting/marriage", json=valid_body()).json()
    assert set(payload) == _ENVELOPE_FIELDS
    assert payload["status"] in {"SUCCESS", "PARTIAL", "FAILED"}
    assert _CONSULTATION_FIELDS <= set(payload["data"])
    assert payload["data"]["score"] is None
    assert payload["data"]["grade"] is None
    consultation_id = payload["data"]["consultation_id"]
    summary = client.get(f"/api/v1/consulting/marriage/{consultation_id}/summary").json()["data"]
    assert _SUMMARY_FIELDS <= set(summary)
    report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report").json()["data"]
    assert _REPORT_FIELDS <= set(report)
    assert report["sections"][0]["section_id"] == "identity"
    warning = payload["warnings"][0] if payload["warnings"] else {"code": "", "description": ""}
    assert "code" in warning
    versions = payload["version_bundle"]
    assert versions["api_version"] == API_VERSION


def test_deterministic_serialization() -> None:
    """The same stored consultation serializes identically twice."""
    client, _ = api_client()
    consultation_id = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]["consultation_id"]
    first = client.get(f"/api/v1/consulting/marriage/{consultation_id}").json()
    second = client.get(f"/api/v1/consulting/marriage/{consultation_id}").json()
    assert json.dumps(first["data"], sort_keys=True) == json.dumps(second["data"], sort_keys=True)
    report_a = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report").json()["data"]
    report_b = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report").json()["data"]
    assert json.dumps(report_a, sort_keys=True) == json.dumps(report_b, sort_keys=True)


def test_idempotency_replay_and_conflict() -> None:
    """The same idempotency key does not create a second consultation."""
    client, _ = api_client()
    headers = {"Idempotency-Key": "tv1-b06-key-1"}
    first = client.post("/api/v1/consulting/marriage", json=valid_body(), headers=headers)
    second = client.post("/api/v1/consulting/marriage", json=valid_body(), headers=headers)
    assert first.status_code == 201
    assert second.status_code == 200
    assert first.json()["data"]["consultation_id"] == second.json()["data"]["consultation_id"]
    other = valid_body()
    other["person_a"]["birth_date"] = "1988-02-02"
    conflict = client.post("/api/v1/consulting/marriage", json=other, headers=headers)
    assert conflict.status_code == 409
    assert conflict.json()["status"] == "FAILED"
    assert conflict.json()["errors"][0]["code"] == "CONFLICT"


def test_history_resource_and_pagination() -> None:
    """History lists stored facts and supports cursor pagination."""
    client, _ = api_client()
    first_id = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]["consultation_id"]
    second_id = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]["consultation_id"]
    listing = client.get("/api/v1/consulting/marriage/history")
    assert listing.status_code == 200
    items = listing.json()["data"]["items"]
    ids = {item["consultation_id"] for item in items}
    assert first_id in ids
    assert second_id in ids
    for item in items:
        assert item["score"] is None
        assert item["grade"] is None
        assert item["status"] == "SUCCESS"
        assert "display_identity" in item
    page = client.get("/api/v1/consulting/marriage/history", params={"limit": 1})
    page_data = page.json()["data"]
    assert len(page_data["items"]) == 1
    assert page_data["next_cursor"]
    page_two = client.get(
        "/api/v1/consulting/marriage/history",
        params={"limit": 1, "cursor": page_data["next_cursor"]},
    )
    assert page_two.json()["data"]["items"][0]["consultation_id"] != page_data["items"][0]["consultation_id"]


def test_correlation_identity_labeled_correctly() -> None:
    """Public JSON uses correlation ids, not Canonical-engine-native analysis ids."""
    client, _ = api_client()
    data = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    consultation_id = data["consultation_id"]
    assert data["person_a"]["correlation_id"] == f"{consultation_id}-A"
    assert data["person_b"]["correlation_id"] == f"{consultation_id}-B"
    assert "analysis_id" not in data["person_a"]
    assert "canonical_analysis_id" not in json.dumps(data)
    report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report").json()["data"]
    assert report["metadata"]["person_a_correlation_id"] == f"{consultation_id}-A"


def test_no_api_side_decision_mutation() -> None:
    """GET resources preserve Decision state and recommendation intents."""
    client, container = api_client()
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    consultation_id = created.json()["data"]["consultation_id"]
    stored = api_service(container).get_stored(consultation_id)
    got = client.get(f"/api/v1/consulting/marriage/{consultation_id}").json()["data"]
    assert got["overall_state"] == stored.result.overall.state.value
    assert stored.result.overall.score is None
    assert stored.result.overall.grade is None
    recs = [item.action_type.value for item in stored.result.recommendations]
    assert got["action_themes"] == list(dict.fromkeys(recs))
    report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report").json()["data"]

    assert stored.report_model is not None
    assert [item["section_id"] for item in report["sections"]] == [
        item.section_id for item in customer_sections(stored.report_model)
    ]
    assert stored.narrative is not None
    headline = next(
        block.text
        for section in stored.narrative.sections
        if section.section_id == "overall"
        for block in section.blocks
        if block.block_id == "overall-headline"
    )
    assert got["headline"] == headline
