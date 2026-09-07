"""Live Canonical pair through the public Marriage API."""

from __future__ import annotations

import json
import re

from consulting.marriage.api.service import MarriageConsultationApi
from consulting.marriage.presentation.placeholder import PlaceholderMarriagePresentationAdapter
from consulting.marriage.ui.placeholder import PlaceholderMarriageUILayoutProfile
from tests.consulting.api_fixtures import api_client, valid_body


def test_live_public_api_round_trip() -> None:
    """POST → GET consultation/summary/report preserves B05 semantics."""
    client, container = api_client(live=True)
    created = client.post("/api/v1/consulting/marriage", json=valid_body())
    assert created.status_code == 201
    payload = created.json()
    data = payload["data"]
    consultation_id = data["consultation_id"]
    assert payload["status"] == "SUCCESS"
    assert data["score"] is None
    assert data["grade"] is None
    got = client.get(f"/api/v1/consulting/marriage/{consultation_id}")
    summary = client.get(f"/api/v1/consulting/marriage/{consultation_id}/summary")
    report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report")
    assert got.status_code == 200
    assert summary.status_code == 200
    assert report.status_code == 200
    assert got.json()["data"]["consultation_id"] == consultation_id
    assert summary.json()["data"]["consultation_id"] == consultation_id
    assert report.json()["data"]["consultation_id"] == consultation_id
    assert got.json()["data"]["overall_state"] == data["overall_state"]
    assert summary.json()["data"]["headline"] == data["headline"]
    sections = [item["section_id"] for item in report.json()["data"]["sections"]]
    assert sections[0] == "identity"
    assert "action_plan" in sections
    blob = json.dumps(got.json()["data"]) + json.dumps(summary.json()["data"]) + json.dumps(report.json()["data"])
    assert not re.search(r"\bEV-\d{4}\b", blob)
    assert not re.search(r"\bF-\d{4}\b", blob)
    api = container.api_contract
    assert isinstance(api, MarriageConsultationApi)
    stored = api.get_stored(consultation_id)
    assert stored.result.overall.state.value == data["overall_state"]
    assert [item.action_type.value for item in stored.result.recommendations]
    assert stored.narrative is not None
    assert stored.report_model is not None
    history = client.get("/api/v1/consulting/marriage/history").json()["data"]["items"]
    assert any(item["consultation_id"] == consultation_id for item in history)
    assert isinstance(container.presentation_adapter, PlaceholderMarriagePresentationAdapter)
    assert isinstance(container.ui_layout_profile, PlaceholderMarriageUILayoutProfile)
    try:
        container.ui_layout_profile.descriptor()
        raise AssertionError("ui must remain unimplemented")
    except NotImplementedError:
        pass
    assert "pdf" not in blob.lower()
    assert "docx" not in blob.lower()
    assert "css" not in blob.lower()
