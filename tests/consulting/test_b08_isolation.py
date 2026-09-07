"""TV1-B08 in-memory state isolation. Process-local persistence only."""

from __future__ import annotations

from tests.consulting.api_fixtures import api_client, valid_body


def test_two_consultations_do_not_overwrite_each_other() -> None:
    """Independent POSTs keep distinct ids, states, and recommendation lists."""
    client, container = api_client()
    first = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    other = valid_body(birth_date_b="1988-02-02")
    second = client.post("/api/v1/consulting/marriage", json=other).json()["data"]
    assert first["consultation_id"] != second["consultation_id"]
    stored_first = container.api_contract.get_stored(first["consultation_id"])
    stored_second = container.api_contract.get_stored(second["consultation_id"])
    assert stored_first.history.consultation_id == first["consultation_id"]
    assert stored_second.history.consultation_id == second["consultation_id"]
    assert stored_first.result.consultation_id != stored_second.result.consultation_id


def test_correlation_ids_are_scoped_to_consultation() -> None:
    """A/B correlation ids never leak across consultations."""
    client, _ = api_client()
    first = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    second = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    assert first["person_a"]["correlation_id"].startswith(first["consultation_id"])
    assert second["person_a"]["correlation_id"].startswith(second["consultation_id"])
    assert first["person_a"]["correlation_id"] != second["person_a"]["correlation_id"]
    assert first["person_b"]["correlation_id"] != second["person_b"]["correlation_id"]


def test_customer_and_expert_get_do_not_mutate_stored_decision() -> None:
    """GET customer then GET expert leaves stored findings and overall state intact."""
    client, container = api_client()
    consultation_id = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]["consultation_id"]
    before = container.api_contract.get_stored(consultation_id)
    before_sig = (
        before.result.overall.state,
        [item.finding_id for item in before.result.findings],
        [item.recommendation_id for item in before.result.recommendations],
    )
    client.get(f"/api/v1/consulting/marriage/{consultation_id}")
    client.get(f"/api/v1/consulting/marriage/{consultation_id}?expert=true")
    after = container.api_contract.get_stored(consultation_id)
    after_sig = (
        after.result.overall.state,
        [item.finding_id for item in after.result.findings],
        [item.recommendation_id for item in after.result.recommendations],
    )
    assert before_sig == after_sig


def test_idempotency_keys_are_isolated() -> None:
    """Two keys create two consultations. The same key replays only its own request."""
    client, _ = api_client()
    first = client.post(
        "/api/v1/consulting/marriage",
        json=valid_body(),
        headers={"Idempotency-Key": "tv1-b08-iso-a"},
    )
    second = client.post(
        "/api/v1/consulting/marriage",
        json=valid_body(),
        headers={"Idempotency-Key": "tv1-b08-iso-b"},
    )
    replay = client.post(
        "/api/v1/consulting/marriage",
        json=valid_body(),
        headers={"Idempotency-Key": "tv1-b08-iso-a"},
    )
    assert first.json()["data"]["consultation_id"] != second.json()["data"]["consultation_id"]
    assert replay.status_code == 200
    assert replay.json()["data"]["consultation_id"] == first.json()["data"]["consultation_id"]


def test_repository_not_found_stays_isolated() -> None:
    """A missing lookup does not disturb a stored consultation."""
    client, container = api_client()
    created = client.post("/api/v1/consulting/marriage", json=valid_body()).json()["data"]
    missing = client.get("/api/v1/consulting/marriage/MC-19990101-XXXXXX")
    assert missing.status_code == 404
    stored = container.api_contract.get_stored(created["consultation_id"])
    assert stored.history.consultation_id == created["consultation_id"]
    assert stored.result.overall.score is None
