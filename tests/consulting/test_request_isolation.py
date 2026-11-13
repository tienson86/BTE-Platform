"""Regressions for isolated concurrent consultations and material request identity."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from threading import Barrier
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from consulting.archive_access import identity
from consulting.marriage.api.parse import parse_consultation_request, request_fingerprint
from consulting.marriage.exceptions import MarriageConflictError, MarriageNotFoundError
from tests.consulting.api_fixtures import api_client, api_service, valid_body


def test_concurrent_requests_keep_result_owner_and_snapshot_separate():
    _, container = api_client()
    api = api_service(container)
    barrier = Barrier(2)
    original = api._orchestrator._after_report
    def overlap(session):
        original(session)
        barrier.wait(timeout=20)
    api._orchestrator._after_report = overlap
    def run(name):
        token = identity.set({"user_id": name, "role": "MEMBER"})
        try:
            body = valid_body()
            body["person_a"]["full_name"] = name
            response = api.create_consultation(parse_consultation_request(body))
            stored = api.get_stored(response.consultation_id)
            assert stored.owner_user_id == name
            assert response.result.person_a.display_name == name
            assert response.result.consultation_id == response.consultation_id
            assert stored.request.person_a.full_name == stored.result.person_a.display_name
            return response.consultation_id
        finally:
            identity.reset(token)
    with ThreadPoolExecutor(max_workers=2) as executor:
        ids = list(executor.map(run, ["review-a", "review-b"]))
    assert len(set(ids)) == 2
    token = identity.set({"user_id": "review-a", "role": "MEMBER"})
    try:
        with pytest.raises(MarriageNotFoundError):
            api.get_stored(ids[1])
    finally:
        identity.reset(token)


def test_concurrent_same_key_creates_only_one_profile():
    _, container = api_client()
    api = api_service(container)
    barrier = Barrier(2)
    def run(_):
        token = identity.set({"user_id": "same-owner", "role": "MEMBER"})
        try:
            barrier.wait(timeout=20)
            result = api.create_consultation(parse_consultation_request(valid_body(), idempotency_key="retry"))
            return result.consultation_id, api.last_create_was_replay
        finally:
            identity.reset(token)
    with ThreadPoolExecutor(max_workers=2) as executor:
        values = list(executor.map(run, range(2)))
    assert len({value[0] for value in values}) == 1
    assert sorted(value[1] for value in values) == [False, True]
    assert len(api._repository.list_history()) == 1


@pytest.mark.parametrize("change", ["place", "luck", "shen_sha", "feng_shui", "narrative", "client"])
def test_material_changes_with_same_key_are_conflicts(change):
    _, container = api_client()
    api = api_service(container)
    original = valid_body()
    original["options"] = {"include_luck": True, "include_shen_sha": True, "include_feng_shui_reference": True, "narrative_level": "standard"}
    modified = deepcopy(original)
    if change == "place":
        modified["person_a"]["birth_place"] = {"display_name": "Paris", "longitude": 2.35}
    elif change == "client":
        modified["request_meta"] = {"client": "business_consulting;occupation=retail"}
    else:
        field = {"luck": "include_luck", "shen_sha": "include_shen_sha", "feng_shui": "include_feng_shui_reference", "narrative": "narrative_level"}[change]
        modified["options"][field] = "detailed" if change == "narrative" else False
    token = identity.set({"user_id": "test-owner", "role": "MEMBER"})
    try:
        request = parse_consultation_request(original, idempotency_key="same-key")
        api.create_consultation(request)
        with pytest.raises(MarriageConflictError):
            api.create_consultation(parse_consultation_request(modified, idempotency_key="same-key"))
    finally:
        identity.reset(token)


@pytest.mark.parametrize("value", ["abc", 2026.5, True, 0, 10000, "NaN"])
def test_bad_luck_year_is_client_error(value):
    client, _ = api_client()
    body = valid_body()
    body["options"] = {"luck_window": {"start_year": value, "end_year": 2030}}
    response = client.post("/api/v1/consulting/marriage", json=body)
    assert response.status_code == 400
    assert response.json()["errors"][0]["code"] == "VALIDATION_ERROR"


@pytest.mark.parametrize("value", ["abc", "NaN", "Infinity", True, 181])
def test_bad_longitude_is_client_error(value):
    client, _ = api_client()
    body = valid_body()
    body["person_a"]["birth_place"] = {"longitude": value}
    assert client.post("/api/v1/consulting/marriage", json=body).status_code == 400


def test_marriage_history_excludes_business_before_pagination():
    _, container = api_client()
    api = api_service(container)
    token = identity.set({"user_id": "test-owner", "role": "MEMBER"})
    try:
        marriage = api.create_consultation(parse_consultation_request(valid_body()))
        body = valid_body()
        body["request_meta"] = {"client": "business_consulting;occupation=retail"}
        business = api.create_consultation(parse_consultation_request(body))
        api.save_business_profile(business.consultation_id)
        rows, cursor = api.list_history_page(limit=1)
        assert [row.consultation_id for row in rows] == [marriage.consultation_id]
        assert cursor is None
        business_rows, _ = api.list_business_history_page(cursor=None, limit=1)
        assert [row.history.consultation_id for row in business_rows] == [business.consultation_id]
    finally:
        identity.reset(token)


def test_production_auth_middleware_rejects_anonymous_request():
    from consulting.archive_access import register_consulting_access
    from consulting.marriage.api.http import build_marriage_router
    _, container = api_client()
    api = api_service(container)
    app = FastAPI()
    app.include_router(build_marriage_router(container), prefix="/api/v1")
    register_consulting_access(app, api, None)
    response = TestClient(app).post("/api/v1/consulting/marriage", json=valid_body())
    assert response.status_code == 401
    assert api._repository.list_history() == []
