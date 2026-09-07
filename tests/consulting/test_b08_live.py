"""TV1-B08 live Canonical pairs through the public API."""

from __future__ import annotations

import json
import re

from tests.consulting.api_fixtures import api_client, api_service, valid_body

LIVE_PAIRS = (
    {
        "id": "LIVE-P1",
        "body": valid_body(),
        "note": "Complete hours, 1987-01-21 / 1990-05-15",
    },
    {
        "id": "LIVE-P2",
        "body": valid_body(birth_date_a="1988-02-02", birth_date_b="1990-05-15", time_a="08:15", time_b="14:40"),
        "note": "Materially different complete pair, 1988-02-02 / 1990-05-15",
    },
    {
        "id": "LIVE-P3",
        "body": valid_body(time_a=None, time_b=None),
        "note": "Same civil dates as P1 with both hours unknown",
    },
)


def test_three_live_canonical_pairs_through_full_pipeline() -> None:
    """Inspect semantics of three live Canonical consultations, not merely HTTP 201."""
    client, container = api_client(live=True)
    api = api_service(container)
    seen_states = set()
    for pair in LIVE_PAIRS:
        created = client.post("/api/v1/consulting/marriage", json=pair["body"])
        assert created.status_code == 201, pair["id"]
        payload = created.json()
        data = payload["data"]
        consultation_id = data["consultation_id"]
        assert payload["status"] == "SUCCESS"
        assert data["score"] is None
        assert data["grade"] is None
        assert data["overall_state"]
        seen_states.add(data["overall_state"])
        summary = client.get(f"/api/v1/consulting/marriage/{consultation_id}/summary")
        report = client.get(f"/api/v1/consulting/marriage/{consultation_id}/report")
        assert summary.status_code == 200
        assert report.status_code == 200
        sections = [item["section_id"] for item in report.json()["data"]["sections"]]
        assert sections[0] == "identity"
        assert "compatibility_hero" in sections
        assert "action_plan" in sections
        assert "timing" not in sections or report.json()["data"]["sections"]
        stored = api.get_stored(consultation_id)
        assert stored.result.overall.score is None
        assert stored.result.overall.grade is None
        assert stored.result.evidence
        assert stored.result.findings
        assert all(item.evidence_ids for item in stored.result.findings)
        assert all(item.source_finding_ids for item in stored.result.recommendations)
        assert stored.narrative is not None
        assert stored.report_model is not None
        blob = json.dumps(data) + json.dumps(summary.json()["data"]) + json.dumps(report.json()["data"])
        assert not re.search(r"\bEV-\d{4}\b", blob)
        assert not re.search(r"\bF-\d{4}\b", blob)
        assert "/100" not in blob
        if pair["id"] == "LIVE-P3":
            codes = [item["code"] for item in payload["warnings"]]
            assert "BIRTH_TIME_UNKNOWN" in codes
            assert "birth_time_unknown" in stored.result.limitations
        unavailable = {
            domain
            for domain, decision in (
                ("interaction", stored.result.domains.interaction),
                ("family", stored.result.domains.family),
                ("children", stored.result.domains.children),
            )
            if not decision.availability.available
        }
        assert "interaction" in unavailable
        assert "family" in unavailable
        assert "children" in unavailable
    assert seen_states


def test_live_customer_expert_separation() -> None:
    """Live expert GET adds trace without changing natal Decision."""
    client, container = api_client(live=True)
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    consultation_id = created["consultation_id"]
    customer = client.get(f"/api/v1/consulting/marriage/{consultation_id}").json()["data"]
    expert = client.get(f"/api/v1/consulting/marriage/{consultation_id}?expert=true").json()["data"]
    stored = api_service(container).get_stored(consultation_id)
    assert customer["overall_state"] == expert["overall_state"] == stored.result.overall.state.value
    assert "expert" not in customer
    assert expert["expert"]["finding_references"]
    assert stored.result.overall.score is None
